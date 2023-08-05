import requests
import json
import random
import string
from iso8601 import parse_date
from ..response import ok, error

def _format_card(response):
    if 'card' not in response:
        return {
            'id': '',
            'card_type': '',
            'last_four_digits': '',
            'cardholder': {
                'name': ''
            },
            'expiration_month': '',
            'expiration_year': '',
        }
    else:
        return {
            'id': response['card']['id'],
            'card_type': 'not_found',
            'last_four_digits': response['card']['last_four_digits'],
            'cardholder': {
                'name': response['card']['cardholder']['name']
            },
            'expiration_month': response['card']['expiration_month'],
            'expiration_year': response['card']['expiration_year'],
        }

def _format(response):
    if response['status'] == 'accredited':
        response['status'] = 'approved'
        response['status_detail'] = 'accredited'
    elif response['status'] == 'approved':
        response['status_detail'] = 'not_accredited'
    elif response['status'] == 'rejected':
        response['status_detail'] = 'rejected'
    result = {
        'id': response['site_transaction_id'],
        'transaction_amount': response['amount']/100,
        'date_created': parse_date(response['date']),
        'status': response['status'],
        'status_detail': response['status_detail'],
        'card': _format_card(response),
        'processor': 'decidir'
    }
    return result

class Payment:
    def __init__(self, url, private_key: str, public_key: str, payment_type: str, site_id: str):
        self.url = url
        self.private_key = private_key
        self.public_key = public_key
        self.payment_type = payment_type
        self.site_id = site_id
        self.headers = {
            'apikey': self.private_key,
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
        }

    def create(self, payment_data: dict):
        site_transaction_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        total_amount = round(payment_data['transaction_amount'], 2) * 100  # se multiplica por 100; no acepta decimales
        body = {
            'customer': {
                'id': payment_data['payer']['decidir_id'],
                'email': payment_data['payer']['email']
            },
            'site_transaction_id': site_transaction_id,     # str(uuid4())
            'token': payment_data['token'],
            'payment_method_id': 1,    # Peso Argentino
            'bin': payment_data['bin'],    # primeros 6 digitos de la tarjeta
            'currency': 'ARS',
            'installments': 1,
            'payment_type': self.payment_type,
            'establishment_name': '-',  # opcional
            'sub_payments': []
        }
        if self.payment_type == 'distributed':
            application_fee = round(payment_data['application_fee'], 2) * 100
            body['sub_payments'] = [
                {
                    'site_id': payment_data['seller_site_id'],
                    'installments': 1,
                    'amount': total_amount - application_fee
                }, {
                    'site_id': self.site_id,    # Cadena
                    'installments': 1,
                    'amount': application_fee
                }
            ]
        else:
            body['amount'] = total_amount
            body['site_id'] = self.site_id

        additional_information = [
            'installments',
            'establishment_name'
        ]
        for item in additional_information:
            if item in payment_data.keys():
                body[item] = payment_data[item]

        r = requests.post(self.url + '/payments', headers=self.headers, data=json.dumps(body))
        response = r.json()
        if r.status_code < 400:
            if 'card' in payment_data:
                response['card'] = payment_data['card']
            return ok(_format(response))
        return error(response)

    def get(self, payment_id: str):
        # r = requests.get(self.url + '/payments/{}'.format(payment_id), headers=self.headers)
        # return ok(_format(r.json()))
        filters = {'siteOperationId': payment_id,
                   'expand':'card_data'}
        r = requests.get(self.url + '/payments', params=filters, headers=self.headers)
        list_results = r.json()['response']['results']
        if len(list_results) == 1:
            return _format(list_results[0])
        else:
            return error('error_pago_no_encontrado')

    def search(self, filters: dict) -> dict:
        # El filter puede ser:
        # offset
        # pageSize
        # siteOperationId
        # merchantId
        # dateFrom
        # dateTo
        # site
        r = requests.get(self.url + '/payments', params=filters, headers=self.headers)
        response = r.json()
        response['results'] = [_format(r) for r in response['results']]
        return ok(response)

    def get_payment_methods(self):
        r = requests.get(self.url + '/payment-methods/1', headers=self.headers)
        return r.json()
