# melosboom-backend


#### Example

TBD



### Merchant Login

```html
POST /merchant/login/
```

#### parameters

* bsc_address - string: the  bsc address

#### Returns

```json
{
    "error_code": 1,
    "result": {
        "status": "ok"
    }
}
```



#### Example

TBD

### Merchant Info

```html
POST /merchant/merchant-info/
```


#### parameters

* bsc_address - string: the  bsc address

#### Returns

```json
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
```

#### Example

TBD

### Merchant List

```html
POST /merchant/merchant-list/
```

#### parameters

* bsc_address - string: the  bsc address

#### Returns

```json
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
            ...
            
        ],  
    }
}  
```


#### Example

TBD

### Order List

```html
POST /merchant/order-list/
```

#### parameters

* bsc_address - string: the  bsc address

#### Returns

```json
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
            ...
        ]
    }
}  
```

#### Example

TBD

### Merchant Register

```html
POST /merchant/register/
```

#### parameters

* bsc_address - string: the  bsc address
* invitor - string: the  invitor
* email - string: the  email
* first_name - string: first name
* last_name - string: the  last name
* selfintroduction - string: the  selfintroduction

#### Returns

```json
{
    "error_code": 1,
    "result": {
        "status": "ok"
    }
}
```
#### Example

TBD

### Apply Withdrawal

```html
POST /merchant/apply-withdrawal/
```

#### parameters

* bsc_address - string: the  bsc address
* balance_usdt - decimal: the value of available withdrawal rewards
* withdrawal_amount - decimal: the value of withdrawal rewards
* description - string: the  description

#### Returns

```json
{
    "error_code": 1,
    "result": {
        "status": "ok"
    }
}
```

#### Example

TBD

### Apply Withdrawal

```html
POST /merchant/apply-withdrawal/
```

#### parameters

* bsc_address - string: the  bsc address
* balance_usdt - decimal: the value of available withdrawal rewards
* withdrawal_amount - decimal: the value of withdrawal rewards
* description - string: the  description

#### Returns

```json
{
    "error_code": 1,
    "result": {
        "status": "ok"
    }
}
```

#### Example

TBD

### Withdrawal List

```html
POST /merchant/get-withdrawal-list/
```

#### parameters

Nothing

#### Returns

```json
{
    "error_code": 1,
    "result": {
        "withdrawallist": [
            {
                "id": 1,
                "created_at": 1724723818,
                "items": 0,
                "balance": "0",
                "amount": "0",
                "status": 1
            },
            ...
            
        ]
    }
}
```

#### Example

TBD

### Founding Info

```html
POST /merchant/get-founding-info/
```

#### parameters

*id - int: the  order id

#### Returns

```json
{
    "error_code": 1,
    "result": {
        "id": 1,
        "created_at": 1724723818,//the created timestamp
        "token": "USDT",
        "balance": "0",
        "amount": "0",
        "reviewed_at": 1724748660,//the reviewed timestamp
        "receive_address": "",
        "transaction_id": "",
        "status": 1,
        "description": ""
    }
}

```
#### Example

TBD

### Merchant Info

```html
POST /merchant/get-merchant-info/
```

#### parameters

* bsc_address - string: the  bsc address

#### Returns

```json
{
    "error_code": 1,
    "result": {
        "first_name": "",
        "last_name": "",
        "email": ""
    }
}
```
#### Example

TBD

### Merchant Info

```html
POST /merchant/save-merchant-info/
```

#### parameters

* bsc_address - string: the  bsc address

#### Returns

```json
{
    "error_code": 1,
    "result": {
        "status": "ok"
    }
}
```

#### Example

TBD

### Merchant Manager Login

```html
POST /merchant/merchant-manager-login/
```

#### parameters

* bsc_address - string: the  bsc address

#### Returns

```json
{
    "error_code": 1,
    "result": {
        "status": "ok"
    }
}
```


#### Example

TBD

### Merchant Manager List

```html
POST /merchant/merchant-manager-list/
```

#### parameters

* Nothing

#### Returns

```json
{
    "error_code": 1,
    "result": {
        "bsc_address": "",
        "first_name": "",
        "last_name": "",
        "email": ""
    }
}
```
#### Example

TBD

### Merchant Manager List

```html
POST /merchant/merchant-manager-list/
```

#### parameters

* Nothing

#### Returns

```json
{
    "error_code": 1,
    "result": {
        "first_name": "",
        "last_name": "",
        "email": ""
    }
}

```

