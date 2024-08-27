import logging

from project.utils import http
from .models import Merchant, Withdrawal
from sale.models import NFTSaleInfo
from .forms import LoginForm, RegisterForm, WithdrawalForm, SearchWithdrawalListForm, GetFoundingInfoForm


from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from config import codes
from utils import formatter
from django.db import transaction
from django.db.models import Q

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def login(request, version):
    try:
        form = LoginForm(request.POST)

        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")

        wallet_address = form.cleaned_data["wallet_address"]

        merchant = Merchant.objects.filter(wallet_address=wallet_address).first()

        if not merchant:
            logger.error("invalid wallet address:%s" % wallet_address)
            return http.JsonErrorResponse(error_message="invalid wallet address")
        if merchant.status != codes.Applystatus.NORMAL.value:
            logger.error("Apply not approved:%s" % wallet_address)
            return http.JsonErrorResponse(error_message="Apply not approved")

        result = {"status": "ok"}
        return http.JsonSuccessResponse(result)
    except Exception as e:
        logger.exception("Faile to execute login: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))
    
@csrf_exempt
@require_POST
def get_merchant_info(request, version):
    try:
        form = LoginForm(request.POST)

        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")

        wallet_address = form.cleaned_data["wallet_address"]

        merchant = Merchant.objects.filter(wallet_address=wallet_address).first()
        total_performance = merchant.total_performance
        last_30days_new = merchant.last_30days_new
        super_node_vilad = ""
        if merchant.super_node == codes.SupperNode.YES.value:
            super_node_vilad = merchant.super_node_vilad

        ofaddress = merchant.ofaddress
        ofreward = merchant.ofreward
        usdt_reward = merchant.usdt_reward
        withdrawal_rewards = merchant.withdrawal_rewards
        result = {
            "total_performance": formatter.decimal_to_str(
                total_performance, precision=10
            ),
            "last_30days_new": formatter.decimal_to_str(last_30days_new, precision=10),
            "super_node_vilad": super_node_vilad,
            "ofaddress": ofaddress,
            "ofreward": formatter.decimal_to_str(ofreward, precision=10),
            "usdt_reward": formatter.decimal_to_str(usdt_reward, precision=10),
            "withdrawal_rewards": formatter.decimal_to_str(
                withdrawal_rewards, precision=10
            ),
        }
        return http.JsonSuccessResponse(result)
    except Exception as e:
        logger.exception("Faile to execute login: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))
@csrf_exempt
@require_POST
def get_merchant_list(request, version):
    try:   
        form = LoginForm(request.POST)

        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")   
        
        merchantSet = Merchant.objects.filter(
            super_node=codes.SupperNode.YES.value
        ).order_by("total_performance")[:25]
        merchantlist = []

        if merchantSet:

            for obj in merchantSet:
                merchantlist.append(
                    {
                        "ofaddress": obj.ofaddress,
                        "total_performance": formatter.decimal_to_str(
                            obj.total_performance, precision=10
                        ),
                        "last_30days_new": formatter.decimal_to_str(
                            obj.last_30days_new, precision=10
                        ),
                        "hashrate": formatter.decimal_to_str(
                            obj.hashrate, precision=10
                        ),
                    }
                )
            result = {'merchantlist': merchantlist}
        return http.JsonSuccessResponse(result)
            
    except Exception as e:
        logger.exception("Faile to execute login: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))

@csrf_exempt
@require_POST  
def get_order_list(request, version):  
    try:
        form = LoginForm(request.POST)
        print("exists")
        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")   
        print("exists")
        wallet_address = form.cleaned_data["wallet_address"]
        orderSet = NFTSaleInfo.objects.filter(bsc_address=wallet_address).order_by(
            "created_at"
        )[:10]
        
        orderlist = []
        if orderSet:
            for obj in orderSet:
                orderlist.append(
                    {
                        "order_id": obj.id,
                        "items": obj.product_id,
                        "amount": formatter.decimal_to_str(obj.amount, precision=10),
                        "created_at": obj.created_at,
                    }
                )

        result = {
            "orderlist": orderlist,
        }

        return http.JsonSuccessResponse(result)
    except Exception as e:
        logger.exception("Faile to execute login: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))


@csrf_exempt
@require_POST
@transaction.atomic
def register(request, version):
    try:
        form = RegisterForm(request.POST)
        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")
        wallet_address = form.cleaned_data["wallet_address"]

        exists = Merchant.objects.filter(wallet_address=wallet_address).exists()
        print("exists")
        print(exists)
        if exists:
            logger.error("wallet address already exists:%s" % str(wallet_address))
            return http.JsonErrorResponse(error_message="wallet address already exists")

        invite_code = form.cleaned_data["invite_code"]
        email = form.cleaned_data["email"]
 
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        selfintroduction = form.cleaned_data["selfintroduction"]

        merchant = Merchant.objects.create(
            wallet_address=wallet_address,
            invite_code=invite_code,
            email=email,
            first_name=first_name,
            last_name=last_name,
            selfintroduction=selfintroduction,
        )

        merchant.save()

        result = {"status": "ok"}
        return http.JsonSuccessResponse(result)

    except Exception as e:
        logger.exception("Faile to execute register: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))
    

@csrf_exempt
@require_POST
@transaction.atomic
def apply_withdrawal(request, version):
    try:
        form = WithdrawalForm(request.POST)
        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")

        my_address = form.cleaned_data["my_address"]
        print(my_address)
        balance_usdt = form.cleaned_data["balance_usdt"]
        withdrawal_amount = form.cleaned_data["withdrawal_amount"]
        description = form.cleaned_data["description"]

        withdrawal = Withdrawal.objects.create(
            my_address=my_address,
            balance=balance_usdt,
            amount=withdrawal_amount,
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
def get_withdrawal_list(request, version):
    try:
        '''
        form = WithdrawalListForm(request.POST)
        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")
        '''

        withdrawalSet = Withdrawal.objects.all().order_by('-created_at')[:20]
        if not withdrawalSet:
            logger.error('invalid No Withdrawal Apply:%s' )
            return http.JsonErrorResponse(error_message='No Withdrawal Apply')
        
        withdrawallist = []
        if withdrawalSet:
            for obj in withdrawalSet:
                withdrawallist.append(
                    {
                        'id': obj.id,
                        'created_at': int(obj.created_at.timestamp()),
                        'items': obj.items,
                        'balance': formatter.decimal_to_str(obj.balance, precision=10),
                        'amount': formatter.decimal_to_str(obj.amount, precision=10),
                        'status': obj.status,
                    }
                )

        result = {
            "withdrawallist": withdrawallist,
        }
        return http.JsonSuccessResponse(result)

    except Exception as e:
        logger.exception("Faile to execute register: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))

@csrf_exempt
@require_POST  
def search_withdrawal_list(request, version):
    try:
        print('search_withdrawal_list')

        form = SearchWithdrawalListForm(request.POST)
        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")
        
        start_date =  form.cleaned_data["start_date"]
        end_date =  form.cleaned_data["end_date"]
        status =  form.cleaned_data["status"]
        transation_id =  form.cleaned_data["transation_id"]


        #result = model.objects.filter(filters).order_by('id')
        print('search_withdrawal_list')

        query = Q()
        if start_date is not None:
            if end_date is not None:
                query &= Q(created_at=(start_date, end_date))

        if status is not None:
            query &= Q(status=status)

        if transation_id is not None:
            query &= Q(transaction_id=transation_id)

        searchwithdrawalSet = Withdrawal.objects.filter(query)
        #searchwithdrawalSet = Withdrawal.objects.filter(Q(created_at=(start_date, end_date)) & Q(status=status) & Q(id=transation_id))
        print('search_withdrawal_list')

        if not searchwithdrawalSet:
            logger.error('invalid No Withdrawal Apply:%s' )
            return http.JsonErrorResponse(error_message='No Withdrawal Apply')
        
        searchwithdrawallist = []
        if searchwithdrawalSet:
            for obj in searchwithdrawalSet:
                searchwithdrawallist.append(
                    {
                        'id': obj.id,
                        'created_at': int(obj.created_at.timestamp()),
                        'items': obj.items,
                        'balance': formatter.decimal_to_str(obj.balance, precision=10),
                        'amount': formatter.decimal_to_str(obj.amount, precision=10),
                        'status': obj.status,
                    }
                )

        result = {
            "withdrawallist": searchwithdrawallist,
        }
        return http.JsonSuccessResponse(result)

    except Exception as e:
        logger.exception("Faile to execute register: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))
    
@csrf_exempt
@require_POST  
def get_founding_info(request, version):
    try:
        print('get_founding_info')

        form = GetFoundingInfoForm(request.POST)
        if not form.is_valid():
            logger.error("validate error:%s" % str(form.errors))
            return http.JsonErrorResponse(error_message="validate error")
        
        id  = form.cleaned_data["id"]
        foundinginfoSet =  Withdrawal.objects.filter(id=id)
        foundinginfo = []
        if foundinginfoSet:
            for obj in foundinginfoSet:
                foundinginfo.append(
                    {
                        'id': obj.id,
                        'created_at': int(obj.created_at.timestamp()),
                        'items': obj.items,
                        'balance': formatter.decimal_to_str(obj.balance, precision=10),
                        'amount': formatter.decimal_to_str(obj.amount, precision=10),
                        'aeviewed_at': int(obj.updated_at.timestamp()),
                        'receive_address': obj.my_address,
                        'transaction_id': obj.transaction_id,
                        'status': obj.status,
                        'description': obj.description,
                    }
                )

        result = {
            "foundinginfo": foundinginfo,
        }

        return http.JsonSuccessResponse(result)

    except Exception as e:
        logger.exception("Faile to execute register: %s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))
    