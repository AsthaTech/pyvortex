# Vortex API Python Client

# Installation 

```
pip install vortex-api
```


# Api Usage 

```python 
from vortex_api import AsthaTradeVortexAPI
from vortex_api import Constants as Vc

client = AsthaTradeVortexAPI("your api secret","your application id")

#For client login using TOTP
client.login("client code","client password","totp")

# Place order 

client.place_order(
       exchange = Vc.ExchangeTypes.NSE_EQUITY,
       token = 22,
       transaction_type =  Vc.TransactionSides.BUY,
       product = Vc.ProductTypes.DELIVERY,
       variety = Vc.VarietyTypes.REGULAR_LIMIT_ORDER,
       quantity = 1,
       price = 1700.0,
       trigger_price=0.0,
       disclosed_quantity= 0,
       validity = Vc.ValidityTypes.FULL_DAY)

#Get order book 
client.orders(limit=20,offset=1)


```
Refer to the [python document](https://vortex.asthatrade.com/docs/pyvortex/vortex_api.html) for all methods and features

