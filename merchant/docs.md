**Merchant Login**

    POST /merchant/login/


**parameters**  
• wallet_address - string: the address of BSC chain
  
**Returns**  

    {
        "error_code": 1,
        "result": {
            "status": "ok"
        }
    }

**Merchant Info**  

    POST /merchant/merchant-info/
    
**Returns**  

    {  

        "error_code": 1,  
        
        "result": {  
        
            "total_performance": "0",  
            "last_30days_new": "0",  
            "super_node_vilad": null,  
            "ofaddress": 0,  
            "ofreward": "0",  
            "usdt_reward": "0",  
            "withdrawal_rewards": "0",  
            
        }
    }  
**Merchant List**  

     POST /merchant/merchant-list/
     
**Returns**

    {  

        "error_code": 1,  
        
        "result": {  

            "merchantlist": [  
            
                {  
                    "ofaddress": 0,  
                    "total_performance": "0",  
                    "last_30days_new": "0",  
                    "hashrate": "0"  
                },  
                
            ],  
        }
    }  
**Order List**  
    
     POST /merchant/order-list/
     
**Returns**  
    {  

        "error_code": 1,  
        
        "result": {  
 
            "orderlist": [
                {
                    "order_id": 0,
                    "items": "0",
                    "amount": 0,
                    "created_at": null
                },
            ]
        }
    }  

**Merchant Register**

    POST /merchant/register/

**parameters**
  
• wallet_address - string: the address of BSC chain  
• invite_code  
• email  
• first_name  
• last_name  
• selfintroduction  
**Returns**  

    {
        "error_code": 1,
        "result": {
            "status": "ok"
        }
    }

**Apply Withdrawal**
  
    POST /merchant/apply-withdrawal/

**parameters**

  
• my_address  
• balance_usdt  
• withdrawal_amount  
• description  

**Returns**  

    {
        "error_code": 1,
        "result": {
            "status": "ok"
        }
    }
