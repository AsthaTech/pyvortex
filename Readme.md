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

# Connecting to websocket

Using the feed, you can listen to both price quote changes and order/trade updates. You need to define your own callbacks for `on_price_update`
and `on_order_update`. The packet structure for `on_order_update` is the same as that received in postbacks and is available [here](https://vortex.asthatrade.com/docs/postbacks/)

```
from vortex_api import VortexFeed
from vortex_api import Constants as Vc
import time

def main():
    # Get access token from any of the login methods
    wire = VortexFeed(access_token) 

    wire.on_price_update = on_price_update
    wire.on_order_update = on_order_update
    wire.on_connect = on_connect
    wire.connect(threaded=True) 
    # If you make threaded = False, anything after this line will not execute

    time.sleep(10)
    
    wire.unsubscribe(Vc.ExchangeTypes.NSE_EQUITY, 26000)
    wire.unsubscribe(Vc.ExchangeTypes.NSE_EQUITY, 26009)
    wire.unsubscribe(Vc.ExchangeTypes.NSE_EQUITY, 2885)


def on_price_update(ws,data): 
    print(data)

def on_order_update(ws,data): 
    print(data)

def on_connect(ws, response):
    ws.subscribe(Vc.ExchangeTypes.NSE_EQUITY, 26000, Vc.QuoteModes.LTP) #Subscribe to NIFTY 
    ws.subscribe(Vc.ExchangeTypes.NSE_EQUITY, 26009,Vc.QuoteModes.OHLCV) # Subscribe to BANKNIFTY 
    ws.subscribe(Vc.ExchangeTypes.NSE_EQUITY, 2885,Vc.QuoteModes.FULL) # Subscribe to RELIANCE 

if __name__ == "__main__":
    main()

```
Refer to the [python document](https://vortex.asthatrade.com/docs/pyvortex/vortex_api.html) for all methods and features

