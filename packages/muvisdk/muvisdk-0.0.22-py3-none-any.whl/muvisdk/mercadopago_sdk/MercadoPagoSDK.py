import mercadopago
from .Customer import Customer
from .Card import Card
from .CardToken import CardToken
from .Payment import Payment
from .Refund import Refund

class MercadoPagoSDK:
    def __init__(self, merchant, marketplace=False):
        if 'credentials' in merchant:
            if not marketplace:
                access_token = merchant['credentials']['mercadopago']['access_token']
            else:
                access_token = merchant['credentials']['mp_marketplace']['access_token']
        else:
            access_token = merchant['keys']['access_token']
        self.sdk = mercadopago.SDK(access_token)
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
