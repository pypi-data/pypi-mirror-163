import mercadopago
from .Customer import Customer
from .Card import Card
from .CardToken import CardToken
from .Payment import Payment
from .Refund import Refund


class MercadoPagoSDK:
    def __init__(self, merchant, marketplace=False):
        active = True
        if 'credentials' in merchant:
            if not marketplace:
                access_token = merchant['credentials']['mercadopago']['access_token']
                active = merchant['credentials']['mercadopago']['active']
            else:
                access_token = merchant['credentials']['mp_marketplace']['access_token']
                active = merchant['credentials']['mp_marketplace']['active']
        else:
            if not marketplace:
                access_token = merchant['keys']['access_token']
            else:
                access_token = merchant['keys_marketplace']['access_token']
        self.sdk = mercadopago.SDK(access_token) if active else None
        self.merchant_id = merchant['_id']
        self.merchant_name = merchant['name']

    def customer(self):
        return Customer(self.sdk)
    
    def card(self):
        return Card(self.sdk)

    def card_token(self):
        return CardToken(self.sdk)
    
    def payment(self):
        return Payment(self.sdk)

    def refund(self):
        return Refund(self.sdk)

    def ok(self):
        return self.sdk is not None
