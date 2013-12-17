from hashlib import md5
from urllib import urlparse, urlencode
from urlparse import parse_qs

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.datastructures import SortedDict
from django.utils.importlib import import_module

from payonline.models import PaymentData
from payonline.settings import CONFIG


class PayonlineTestCase(TestCase):

    def setUp(self):
        self.url = reverse('payonline_callback')
        self.old_config = CONFIG
        CONFIG['PRIVATE_SECURITY_KEY'] = '123'
        CONFIG['MERCHANT_ID'] = '1'

    def tearDown(self):
        CONFIG = self.old_config

    def get_form_data(self, **kwargs):
        data = {
            'DateTime': '2013-08-01 14:24:31',
            'TransactionID': '1',
            'OrderId': '125',
            'Amount': '125.00',
            'Currency': 'RUB',
            'Provider': 'Card',
            'SecurityKey': 'dc68debbb39ede71d786b2d49f40a9e8'
        }
        data.update(**kwargs)
        return data


class CallbackTestCase(PayonlineTestCase):

    def test_get_callback(self):
        response = self.client.get(self.url, data=self.get_form_data())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PaymentData.objects.filter(transaction_id=1).exists())

    def test_post_callback(self):
        response = self.client.post(self.url, data=self.get_form_data())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PaymentData.objects.filter(transaction_id=1).exists())

    def test_invalid_callback(self):
        response = self.client.post(self.url, data=self.get_form_data(
            Currency='USD',
        ))
        self.assertEqual(response.status_code, 400)
        self.assertFalse(PaymentData.objects.filter(transaction_id=1).exists())


class PayTestCase(PayonlineTestCase):

    def setUp(self):
        super(PayTestCase, self).setUp()
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

        session = self.client.session
        session['payonline_order_id'] = 213
        session['payonline_amount'] = '550'
        session.save()

        self.url = reverse('payonline_pay')

    def test_redirect(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        target = response['Location']
        query = urlparse(target).query
        query = parse_qs(query)
        data = SortedDict()
        data['MerchantId'] = query.get('MerchantId', [''])[0]
        data['OrderId'] = query.get('OrderId', [''])[0]
        data['Amount'] = query.get('Amount', [''])[0]
        data['Currency'] = query.get('Currency', [''])[0]
        data['PrivateSecurityKey'] = CONFIG['PRIVATE_SECURITY_KEY']
        SecurityKey = md5(urlencode(data)).hexdigest()
        self.assertEqual(query['SecurityKey'][0], SecurityKey)
