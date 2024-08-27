from django import forms

class LoginForm(forms.Form):
    print('LoginForm')
    wallet_address = forms.CharField(required=True, max_length=128)
    print('LoginForm')

class RegisterForm(forms.Form):
    invite_code = forms.CharField(required=True, max_length=8)
    email = forms.EmailField(required=True, max_length=128)
    first_name = forms.CharField(required=True, max_length=128)
    last_name = forms.CharField(required=True, max_length=128)
    selfintroduction = forms.CharField(required=False,max_length=200)
    wallet_address = forms.CharField(required=True,max_length=128)

class WithdrawalForm(forms.Form):
    my_address = forms.CharField(required=False,max_length=128)
    balance_usdt = forms.DecimalField(required=True, max_digits=20, decimal_places=2)
    withdrawal_amount = forms.DecimalField(required=True, max_digits=20, decimal_places=2)
    description = forms.CharField(required=False, max_length=128)
    '''
class WithdrawalListForm(forms.Form):
    start_date = forms.DateField(required=False,max_length=128)
    end_date = forms.DateField(required=False,max_length=128)
    status = forms.IntegerField(required=False,max_length=128)
    transation_id = forms.CharField(required=False,max_length=128)
    '''

class SearchWithdrawalListForm(forms.Form):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    status = forms.IntegerField(required=False)
    transation_id = forms.CharField(required=False)


class GetFoundingInfoForm(forms.Form):
        id = forms.IntegerField(required=True)