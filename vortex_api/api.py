import requests

class AsthaTradeVortexAPI:

    #Constants 

    #Exchanges
    EXCHANGE_NSE_FO = "NSE_FO"
    EXCHANGE_NSE_EQUITY = "NSE_EQ"
    EXCHANGE_NSE_CURRENCY = "NSE_CD"
    EXCHANGE_MCX = "MCX_FO"

    #Variety 
    VARIETY_REGULAR_LIMIT_ORDER = "RL"
    VARIETY_REGULAR_MARKET_ORDER = "RL-MKT"
    VARIETY_STOP_LIMIT_ORDER = "SL"
    VARIETY_STOP_MARKET_ORDER = "SL-MKT"

    #Product 
    PRODUCT_INTRADAY = "INTRADAY"
    PRODUCT_DELIVERY = "DELIVERY"
    PRODUCT_MTF = "MTF"

    #Validity 
    VALIDITY_FULL_DAY = "DAY"
    VALIDITY_IMMEDIATE_OR_CANCEL = "IOC"
    VALIDITY_AFTER_MARKET = "AMO"

    # Transaction type
    TRANSACTION_TYPE_BUY = "BUY"
    TRANSACTION_TYPE_SELL = "SELL"
    

    def __init__(self, api_key: str, application_id: str, base_url: str = "https://vortex.restapi.asthatrade.com") -> None:
        """
        Constructor method for AsthaTradeAPI class.

        Args:
            api_key (str): API key for the Astha Trade API.
            api_secret (str): API secret for the Astha Trade API.
            base_url (str, optional): Base URL for the Astha Trade API. Defaults to "https://vortex.restapi.asthatrade.com".
        """
        self.api_key = api_key
        self.application_id = application_id
        self.base_url = base_url
        self.access_token = None

    def _make_api_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """
        Private method to make HTTP requests to the Astha Trade API.

        Args:
            method (str): HTTP method for the request (e.g. "GET", "POST", "PUT", "DELETE").
            endpoint (str): API endpoint for the request.
            data (dict, optional): Payload data for the request. Defaults to None.

        Returns:
            dict: Dictionary containing the response data from the API.
        """
        if(self.access_token == None):
            op = {}
            op["status"]= "error"
            op["message"] = "please login first"
            return op
        bearer_token = f"Bearer {self.access_token}"
        headers = {"Content-Type": "application/json", "Authorization": bearer_token}
        url = self.base_url + endpoint
        response = requests.request(method, url, headers=headers, json=data)

        response.raise_for_status()
        print(response.text)
        return response.json()
    
    def _make_unauth_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """
        Private method to make HTTP requests to the Astha Trade API.

        Args:
            method (str): HTTP method for the request (e.g. "GET", "POST", "PUT", "DELETE").
            endpoint (str): API endpoint for the request.
            data (dict, optional): Payload data for the request. Defaults to None.

        Returns:
            dict: Dictionary containing the response data from the API.
        """
        headers = {"Content-Type": "application/json", "x-api-key": self.api_key}
        print(headers)
        url = self.base_url + endpoint
        response = requests.request(method, url, headers=headers, json=data)

        response.raise_for_status()
        return response.json()

    def login(self, client_code: str, password: str, totp: str)->dict:
        """
        Login using password and totp directly

        Args:
            client_code(str): Client Code of the account
            password(str): Password of the account
            totp(str): TOTP generated using third party apps like google authenticator etc. 

        Returns:
            dict: JSON response containing the details of the user
        """
        endpoint = "/user/login"
        data = {
            "client_code": client_code,
            "password": password,
            "totp": totp,
            "application_id": self.application_id
        }
        res = self._make_unauth_request("POST", endpoint, data=data)
        self._setup_client_code(login_object=res)
    def place_order(self,exchange: str, token: int, transaction_type: str, product: str, variety: str, 
                quantity: int, price: float, trigger_price: float, disclosed_quantity: int, validity: str, 
                validity_days: int, is_amo: bool) -> dict:
        """
        Place an order for a specific security

        Args:
            exchange (str): Possible values: [NSE_EQ, NSE_FO, NSE_CD or MCX_FO]
            token (int): Security token of the scrip. It can be found in the scripmaster file
            transaction_type (str): Possible values: [BUY, SELL]
            product (str): Possible values: [INTRADAY, DELIVERY, MTF]. MTF product can only be used in NSE_EQ exchange.
            variety (str): Possible values: [RL, RL-MKT, SL, SL-MKT]. RL means regular orders, SL means Stop Loss order. 
                        MKT means that the trade will happen at market price
            quantity (int): For exchange NSE_FO, if you want to trade in 2 lots and lot size is 50, you should pass 100. 
                            In all other exchanges, you should pass just the number of lots. For example, in MCX_FO, 
                            if you want to trade 5 lots, you should pass just 5.
            price (float): Price should be an integer multiple of Tick Size. For example, IDEA's tick size is 0.05. 
                        So the price entered can be 9.5 or 9.65. It cannot be 9.67. 
                        In case of market orders, you should send the Last Trade Price received from the Quote API or Websocket API
            trigger_price (float): To be used for Stop loss orders. For BUY side SL orders, trigger_price should be 
                                lesser than price. for SELL side SL orders, trigger_price should be greater than price.
            disclosed_quantity (int): Can be any number lesser than or equal to quantity, including 0
            validity (str): Can be DAY for orders which are valid throughout the day, or IOC. 
                            IOC order will be cancelled if it is not traded immediately
            validity_days (int): Number of days for which the order is valid. Required only if validity is set to DAY.
            is_amo (bool): Possible values: [true,false]. Should be set to true if order is being placed after market hours

        Returns:
            dict: JSON response containing the details of the placed order

        Raises:
            HTTPError: If any HTTP error occurs during the API call
        """

        endpoint = "/orders/regular"

        data = {
            "exchange": exchange,
            "token": token,
            "transaction_type": transaction_type,
            "product": product,
            "variety": variety,
            "quantity": quantity,
            "price": price,
            "trigger_price": trigger_price,
            "disclosed_quantity": disclosed_quantity,
            "validity": validity,
            "validity_days": validity_days,
            "is_amo": is_amo
        }
        
        return self._make_api_request("POST", endpoint, data=data)
    
    def modify_order(self,exchange: str, order_id: str, variety: str, quantity: int, traded_quantity: int, price: float, trigger_price: float, disclosed_quantity: int, validity: str, validity_days: int) -> dict:
        """
        Method to modify an order using the Astha Trade API.

        Args:
            exchange (str): Possible values: [NSE_EQ, NSE_FO, NSE_CD or MCX_FO]
            order_id (str): The unique ID of the order to modify.
            variety (str): Possible values: [RL, RL-MKT, SL, SL-MKT]. RL means regular orders, SL means Stop Loss order. 
                    MKT means that the trade will happen at market price
            quantity (int): The new quantity for the order.
            traded_quantity (int): The quantity of the order that has already been traded.
            price (float): The new price for the order.
            trigger_price (float): The new trigger price for the order. Required for SL and SL-M orders.
            disclosed_quantity (int): The new quantity to be disclosed publicly.
            validity (str): The new validity for the order (e.g. DAY, IOC, GTD).
            validity_days (int): The number of days the order is valid for. Required for GTD validity.

        Returns:
            dict: Dictionary containing the response data from the API.
        """
        endpoint = f"/orders/regular/{exchange}/{order_id}"
        data = {
            "variety": variety,
            "quantity": quantity,
            "traded_quantity": traded_quantity,
            "price": price,
            "trigger_price": trigger_price,
            "disclosed_quantity": disclosed_quantity,
            "validity": validity,
            "validity_days": validity_days
        }
        return self._make_api_request("PUT", endpoint, data=data)
    
    def cancel_order(self,exchange: str, order_id: str) -> dict:
        """
        Method to cancel an order using the Astha Trade API.

        Args:
            exchange (str): Possible values: [NSE_EQ, NSE_FO, NSE_CD or MCX_FO]
            order_id (str): The unique ID of the order to cancel.

        Returns:
            dict: Dictionary containing the response data from the API.
        """
        
        endpoint = f"/orders/regular/{exchange}/{order_id}"
        return self._make_api_request("DELETE", endpoint)

    def orders(self,limit: int, offset: int) -> dict:
        """
        Method to get the position book using the Astha Trade API.

        Args:
            limit (int): Limit is the number of orders to be fetched. 
            offset (int): Offset should atleast be 1 

        Returns:
            dict: Dictionary containing the response data from the API.
        """
        endpoint = f"/orders?limit={limit}&offset={offset}"
        return self._make_api_request("GET", endpoint)
    
    def positions(self) -> dict:
        """
        Method to get the position book using the Astha Trade API.

        Returns:
            dict: Dictionary containing the response data from the API.
        """
        endpoint = f"/portfolio/positions"
        return self._make_api_request("GET", endpoint)
    
    def holdings(self) -> dict:
        """
        Method to get the holdings of the user using the Astha Trade API.

        Returns:
            dict: Dictionary containing the response data from the API.
        """
        endpoint = "/portfolio/holdings"
        return self._make_api_request("GET", endpoint)
    
    def funds(self) -> dict:
        """
        Method to get the holdings of the user using the Astha Trade API.

        Returns:
            dict: Dictionary containing the response data from the API.
        """
        endpoint = "/user/funds"
        return self._make_api_request("GET", endpoint)
    
    
    def get_order_margin(self, exchange: str, token: int, transaction_type: str, product: str, variety: str, 
                     quantity: int, price: float, trigger_price: float, disclosed_quantity: int, validity: str, 
                     validity_days: int, is_amo: bool,mode: str) -> dict:
        """
        Get the margin required for placing an order for a specific security.

        Args:
            exchange (str): Possible values: [NSE_EQ, NSE_FO, NSE_CD or MCX_FO]
            token (int): Security token of the scrip. It can be found in the scripmaster file
            transaction_type (str): Possible values: [BUY, SELL]
            product (str): Possible values: [INTRADAY, DELIVERY, MTF]. MTF product can only be used in NSE_EQ exchange.
            variety (str): Possible values: [RL, RL-MKT, SL, SL-MKT]. RL means regular orders, SL means Stop Loss order. 
                        MKT means that the trade will happen at market price
            quantity (int): For exchange NSE_FO, if you want to trade in 2 lots and lot size is 50, you should pass 100. 
                            In all other exchanges, you should pass just the number of lots. For example, in MCX_FO, 
                            if you want to trade 5 lots, you should pass just 5.
            price (float): Price should be an integer multiple of Tick Size. For example, IDEA's tick size is 0.05. 
                        So the price entered can be 9.5 or 9.65. It cannot be 9.67. 
                        In case of market orders, you should send the Last Trade Price received from the Quote API or Websocket API
            trigger_price (float): To be used for Stop loss orders. For BUY side SL orders, trigger_price should be 
                                lesser than price. for SELL side SL orders, trigger_price should be greater than price.
            disclosed_quantity (int): Can be any number lesser than or equal to quantity, including 0
            validity (str): Can be DAY for orders which are valid throughout the day, or IOC. 
                            IOC order will be cancelled if it is not traded immediately
            validity_days (int): Number of days for which the order is valid. Required only if validity is set to DAY.
            is_amo (bool): Possible values: [true,false]. Should be set to true if order is being placed after market hours
            mode(str): Possible values: [NEW, MODIFY] , Whether you are trying to modify an existing order or placing a new order.

        Returns:
            dict: JSON response containing the details of the margin required to place the order

        Raises:
            HTTPError: If any HTTP error occurs during the API call
        """
        
        endpoint = "/margins/order"
        
        data = {
            "exchange": exchange,
            "token": token,
            "transaction_type": transaction_type,
            "product": product,
            "variety": variety,
            "quantity": quantity,
            "price": price,
            "trigger_price": trigger_price,
            "disclosed_quantity": disclosed_quantity,
            "validity": validity,
            "validity_days": validity_days,
            "mode": mode,
            "is_amo": is_amo
        }
        return self._make_api_request("POST", endpoint, data=data)
    
    def _setup_client_code(self, login_object: dict) -> bool: 
        """ 
        Sets up access token after login

        Args: 
            login_object(dict): Login object received

        Returns: 
            (bool): Whether successful or not
        """

        if (('data' in login_object ) and login_object["data"] != None and login_object["data"]["access_token"] != None): 
            self.access_token = login_object["data"]["access_token"]
            return True
        
        return False