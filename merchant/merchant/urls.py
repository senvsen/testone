from django.urls import path

from .api import *
print('urlpatterns')

urlpatterns = [
    
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('merchant-info/', get_merchant_info, name='get_merchant_info'),
    path('merchant-list/', get_merchant_list, name='get_merchant_list'),
    path('order-list/', get_order_list, name='get_order_list'),
    path('apply-withdrawal/', apply_withdrawal, name='apply_withdrawal'),
    path('get-withdrawal-list/', get_withdrawal_list, name='get_withdrawal_list'),
    path('search-withdrawal-list/', search_withdrawal_list, name='search_withdrawal_list'),
    path('get-founding-info/', get_founding_info, name='get_founding_info'),
    #path('get-order-info/', get_order_info, name='get_order_info'),
    #path('get-user-info/', get_user_info, name='get_user_info'),
    #path('save-user-info/', save_user_info, name='save_user_info'),
    
]