# Vortex API Python Client

# Installation 

```
pip install vortex-api
```


# Api Usage 

```python 
from vortex_api import AsthaTradeVortexAPI

client = AsthaTradeVortexAPI("your api secret","your application id")

#For client login using TOTP
client.login("client code","client password","totp")

# Place order 

client.place_order(client.EXCHANGE_NSE_EQUITY,22,client.TRANSACTION_TYPE_BUY,client.PRODUCT_DELIVERY,client.VARIETY_REGULAR_LIMIT_ORDER,1,1700,0,0,"DAY",1,True)

#Get order book 
client.orders(limit=20,offset=1)


```
Refer to the [python document](https://vortex.asthatrade.com/docs/pyvortex/vortex_api.html) for all methods and features

