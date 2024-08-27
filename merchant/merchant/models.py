from django.db import models
from config import codes

# Create your models here.


class Merchant(models.Model):
    id = models.AutoField(primary_key=True)
    wallet_address = models.CharField(max_length=128, unique=True)
    email = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    
    status = models.IntegerField(default=codes.ApplyStatus.NORMAL.value)
    total_performance = models.DecimalField(max_digits=26, decimal_places=18, default=0)
    last_30days_new = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    super_node = models.IntegerField(default=codes.SupperNode.YES.value)
    super_node_vilad = models.DateTimeField(null=True, blank=True)
    ofaddress = models.IntegerField(default=0)
    hashrate = models.DecimalField(max_digits=26, decimal_places=2, default=0)
    ofreward = models.DecimalField(max_digits=26, decimal_places=18, default=0)
    usdt_withdraw = models.DecimalField(max_digits=26, decimal_places=18, default=0)
    usdt_reward = models.DecimalField(max_digits=26, decimal_places=18, default=0)
    withdrawal_rewards = models.DecimalField(
        max_digits=26, decimal_places=18, default=0
    )
    boom = models.DecimalField(max_digits=26, decimal_places=18, default=0)
    boom_incoming = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    boom_cooloff = models.DecimalField(max_digits=26, decimal_places=18, default=0)
    bomm_staking = models.DecimalField(max_digits=26, decimal_places=18, default=0)
    bomm_withdraw = models.DecimalField(max_digits=26, decimal_places=18, default=0)
    total_reward = models.DecimalField(max_digits=26, decimal_places=18, default=0)
    usdt_staking = models.DecimalField(max_digits=26, decimal_places=18, default=0)
    usdt_deposit = models.DecimalField(max_digits=26, decimal_places=18, default=0)
    aispeakernft = models.IntegerField(default=0)
    staking_aispeakernft = models.IntegerField(default=0)
    bitsboomnft = models.IntegerField(default=0)
    staking_bitsboomnft = models.IntegerField(default=0)
    
    invite_code = models.CharField(max_length=8, default="", blank=True)
    selfintroduction = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "merchant"

class Withdrawal(models.Model):
    
    id = models.AutoField(primary_key=True)
    
    my_address = models.CharField(max_length=128,default = '')
    items = models.IntegerField(default=0)
    #quantity = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=26, decimal_places=18, default=0)
    amount = models.DecimalField(max_digits=26, decimal_places=18, default=0)
    status = models.IntegerField(default=codes.WithdrawalStatus.PENDING.value)
    transaction_id = models.CharField(max_length=128, blank=True)
    #action = models.IntegerField(default=codes.WithdrawalStatus.PENDING.value)
    description = models.CharField(max_length=128, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

