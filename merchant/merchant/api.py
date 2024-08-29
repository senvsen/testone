import logging

from project.utils import http
from .models import Agency, Withdraw
from sale.models import NFTSaleInfo
from user.models import User
from power.models import DepositPerformanceIncrement
from .forms import LoginForm, AgencyInfoForm, OrderListForm, RegisterForm, AgencyWithdraw, AgencyWithdrawListForm
from .forms import EditEgencyForm, WithdrawInfoForm, WithdrawDelForm

from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import timedelta
from django.utils.timezone import now

from config import codes
from utils import ecc_tools, formatter, auth, check, decorators
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import Q

logger = logging.getLogger(__name__)



@csrf_exempt
@require_POST
@decorators.agency_required
def login(request, version):
    try:
        form = LoginForm(request.POST)

        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")

        bsc_address = form.cleaned_data["bsc_address"]
        if not check.is_evm_address(bsc_address):
            logger.error(f'validate error: error address {bsc_address}')
            return http.JsonErrorResponse(error_message='validate error')

        sign_message = form.cleaned_data['sign_message']
        signature = form.cleaned_data['signature']

        # validate sign message
        if bsc_address != sign_message:
            return http.JsonErrorResponse(error_message="invalid sign message")
        # validate signature
        if not ecc_tools.verify_evm_signature(bsc_address, sign_message, signature):
            return http.JsonErrorResponse(error_message="invalid signature")

        agency = Agency.objects.filter(bsc_address=bsc_address).first()

        if not agency:
            logger.error("invalid wallet address:%s" % bsc_address)
            return http.JsonErrorResponse(error_message="invalid wallet address")
        if agency.status == codes.AgencyStatus.AUDITING.value:
            logger.error("Apply not approved:%s" % bsc_address)
            return http.JsonErrorResponse(error_message="Apply not approved")
        if agency.status == codes.AgencyStatus.LOCK.value:
            logger.error("acount is locked:%s" % bsc_address)
            return http.JsonErrorResponse(error_message="acount is locked")

        # create jwt token
        token = auth.create_jwt_token_from_address(bsc_address)
        # response
        result = {
            "token": token,
        }
        return http.JsonSuccessResponse(result)
    except Exception as e:
        logger.exception("Faile to execute login: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))

@csrf_exempt
@require_POST
@decorators.agency_required
def get_agency_info(request, version):
    try:
        form = AgencyInfoForm(request.POST)

        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")

        bsc_address = form.cleaned_data["bsc_address"]
        if not check.is_evm_address(bsc_address):
            return http.JsonErrorResponse(error_message='invalid bsc address')
        
        agency = Agency.objects.filter(bsc_address=bsc_address).first()
        email = agency.email,
        first_name = agency.first_name,
        last_name = agency.last_name,

        user = User.objects.filter(bsc_address=bsc_address).first()
        total_performance = user.total_deposite_amount
        total_commission_amount = agency.total_commission_amount
        claimable_commission_amount = agency.claimable_commission_amount

        current_date = now()
        thirty_days_ago = current_date - timedelta(days=30)
        thirty_days_ago.strftime('%Y-%m-%d-%H')

        last_30days_new = DepositPerformanceIncrement.objects.filter(date__gte=thirty_days_ago.strftime('%Y-%m-%d-%H')).aggregate(sum=Coalesce(Sum('increment_amount'),Decimal(0)))['sum']

        withdraw_commission_amount = Withdraw.objects.aggregate(total=Sum('amount'))['total']

        result = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "total_performance": formatter.decimal_to_str(total_performance, precision=10),
            "last_30days_new": formatter.decimal_to_str(last_30days_new, precision=10),
    
            "total_commission_amount": formatter.decimal_to_str(total_commission_amount, precision=10),
            "claimable_commission_amount": formatter.decimal_to_str(claimable_commission_amount, precision=10),
            "withdraw_commission_amount": withdraw_commission_amount,

        }
        return http.JsonSuccessResponse(result)
    except Exception as e:
        logger.exception("Faile to execute login: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))

@csrf_exempt
@require_POST
@decorators.agency_required
def get_agency_order_list(request, version):
    try:
        form = OrderListForm(request.POST)
        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")

        bsc_address = form.cleaned_data["bsc_address"]
        if not check.is_evm_address(bsc_address):
            return http.JsonErrorResponse(error_message='invalid bsc address')
        
        nftsaleinfo = NFTSaleInfo.objects.filter(bsc_address=bsc_address).first()
        order_id = nftsaleinfo.id
        product_id = nftsaleinfo.product_id
        amount = nftsaleinfo.amount
        created_at = nftsaleinfo.created_at
        
        result = {
            "order_id": order_id,
            "product_id": product_id,
            "amount": formatter.decimal_to_str(amount, precision=10),
            "created_at": created_at.strftime('YYYY-MM-DD HH:MM'),

        }

        return http.JsonSuccessResponse(result)
    except Exception as e:
        logger.exception("Faile to execute login: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))

@csrf_exempt
@require_POST
@transaction.atomic
@decorators.agency_required
def register(request, version):
    try:
        form = RegisterForm(request.POST)
        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")
        bsc_address = form.cleaned_data["bsc_address"]
        if not check.is_evm_address(bsc_address):
            return http.JsonErrorResponse(error_message='invalid bsc address')
        
        exists = Agency.objects.filter(bsc_address=bsc_address).exists()
        if exists:
            logger.error("wallet address already exists:%s" % str(bsc_address))
            return http.JsonErrorResponse(error_message="wallet address already exists")

        inviter = form.cleaned_data["inviter"]
        email = form.cleaned_data["email"]
 
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        introduction = form.cleaned_data["introduction"]

        agency = Agency.objects.create(
            bsc_address=bsc_address,
            inviter=inviter,
            email=email,
            first_name=first_name,
            last_name=last_name,
            introduction=introduction,
        )

        agency.save()

        result = {"status": "ok"}
        return http.JsonSuccessResponse(result)
    except Exception as e:
        logger.exception("Faile to execute register: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))

@csrf_exempt
@require_POST
@transaction.atomic
@decorators.agency_required
def agency_withdraw(request, version):
    try:
        form = AgencyWithdraw(request.POST)
        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")
        
        bsc_address = form.cleaned_data["bsc_address"]
        
        if not check.is_evm_address(bsc_address):
            return http.JsonErrorResponse(error_message='invalid bsc address')

        sign_message = form.cleaned_data['sign_message']
        signature = form.cleaned_data['signature']
        # validate sign message
        if bsc_address != sign_message:
            return http.JsonErrorResponse(error_message="invalid sign message")
        # validate signature
        if not ecc_tools.verify_evm_signature(bsc_address, sign_message, signature):
            return http.JsonErrorResponse(error_message="invalid signature")
        
        withdraw_amount = form.cleaned_data["withdraw_amount"]
        description = form.cleaned_data["description"]

        agency = Agency.objects.filter(bsc_address=bsc_address).first()
        claimable_commission_amount = agency.claimable_commission_amount

        withdrawal = Withdraw.objects.create(
            bsc_address=bsc_address,
            balance=claimable_commission_amount,
            amount=withdraw_amount,
            description=description,
        )

        withdrawal.save()

        result = {"status": "ok"}
        return http.JsonSuccessResponse(result)

    except Exception as e:
        logger.exception("Faile to execute register: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))      
    

@csrf_exempt
@require_POST
@decorators.agency_required
def get_agency_withdraw_list(request, version):
    try:
        form = AgencyWithdrawListForm(request.POST)
        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")
        
        bsc_address = form.cleaned_data["bsc_address"]
        if not check.is_evm_address(bsc_address):
            return http.JsonErrorResponse(error_message='invalid bsc address')
        
        withdrawalSet = Withdraw.objects.all().order_by('-created_at')[:20]
        if not withdrawalSet:
            logger.error('invalid No Withdrawal Apply:%s' )
            return http.JsonErrorResponse(error_message='No Withdrawal Apply')
        
        #withdrawallist = []
        if withdrawalSet:
            for obj in withdrawalSet:
                result = {
                    
                        'id': obj.id,
                        'created_at': obj.created_at.strftime('YYYY-MM-DD'),
                        'token_type': obj.token_type,
                        'balance': formatter.decimal_to_str(obj.balance, precision=10),
                        'amount': formatter.decimal_to_str(obj.amount, precision=10),
                        'status': obj.status,
                }

        return http.JsonSuccessResponse(result)

    except Exception as e:
        logger.exception("Faile to execute register: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))      

@csrf_exempt
@require_POST
@decorators.agency_required
def edit_agency_info(request, version):
    try:
        form = EditEgencyForm(request.POST)
        if not form.is_valid():
            logger.error('validate error:%s' % str(form.errors))
            return http.JsonErrorResponse(error_message='validate error')

        bsc_address = form.cleaned_data['bsc_address']
        agency = Agency.objects.filter(bsc_address=bsc_address, status=codes.AgencyStatus.AUDITING.value).first()
        if not agency:
            return http.JsonErrorResponse(error_message='invalid agency status')
        
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        if not check.is_valid_email(email):
            logger.error('invalid email:%s' % str(email))
            return http.JsonErrorResponse(error_message='invalid email')

        agency.first_name = first_name
        agency.last_name = last_name
        agency.email = agency.email
        agency.save()

        result = {
            "status": "ok",
        }
        return http.JsonSuccessResponse(result)
    except Exception as e:
        logger.exception('Faile to excute edit_agency_info: %s' % str(e))
        return http.JsonErrorResponse(error_message=str(e)) 


@csrf_exempt
@require_POST
@decorators.agency_required
def retrieve_withdraw_info(request, version):
    try:
        form = WithdrawInfoForm(request.POST)
        if not form.is_valid():
            logger.error('validate error:%s' % str(form.errors))
            return http.JsonErrorResponse(error_message='validate error')

        bsc_address = form.cleaned_data['bsc_address']
        agency = Agency.objects.filter(bsc_address=bsc_address, status=codes.AgencyStatus.AUDITING.value).first()
        if not agency:
            return http.JsonErrorResponse(error_message='invalid agency status')
        
        id = form.cleaned_data['id']
        withdraw = Withdraw.objects.filter(id=id, bsc_address=bsc_address).first()
        if not withdraw:
            return http.JsonErrorResponse(error_message='failed to get withdraw information')

        created_at = withdraw.created_at.strftime("%Y-%m-%d %H:%M:%S")
        token_type = withdraw.token_type
        balance = withdraw.balance
        amount = withdraw.amount
        reviewed_at = withdraw.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        receive_address = bsc_address
        txid = withdraw.txid
        status = withdraw.status
        description = withdraw.description

        result = {
            "id": id,
            "created_at": created_at,
            "token_type": token_type,
            "balance": formatter.decimal_to_str(balance),
            "amount": formatter.decimal_to_str(amount),
            "reviewed_at": reviewed_at,
            "receive_address": receive_address,
            "txid": txid,
            "status": status,
            "description": description,
        }
        return http.JsonSuccessResponse(result)
    except Exception as e:
        logger.exception('Faile to excute retrieve_withdraw_info: %s' % str(e))
        return http.JsonErrorResponse(error_message=str(e)) 

@csrf_exempt
@require_POST
@decorators.agency_required
def delete_Withdraw(request, version):
    try:
        form = WithdrawDelForm(request.POST)
        if not form.is_valid():
            logger.error('validate error:%s' % str(form.errors))
            return http.JsonErrorResponse(error_message='validate error')
        
        bsc_address = form.cleaned_data['bsc_address']
        id = form.cleaned_data['id']

        withdrawaDel = Withdraw.objects.filter(id=id).first()
        if not withdrawaDel:
            logger.error('invalid No Withdrawal Apply:%s' )
            return http.JsonErrorResponse(error_message='No Withdrawal Apply')
        
        if  withdrawaDel.status != WithdrawStatus.PENDING.value:
            logger.error('invalid Not Pengding status:%s' )
            return http.JsonErrorResponse(error_message='Not Pengding status')
        
        withdrawaDel.status = WithdrawStatus.DELETED.value
        withdrawaDel.save()
        
        result = {
            "status": "ok",
        }
        return http.JsonSuccessResponse(result)
    
    except Exception as e:
        logger.exception('Faile to excute retrieve_withdraw_info: %s' % str(e))
        return http.JsonErrorResponse(error_message=str(e)) 
