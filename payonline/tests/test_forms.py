from django.test import TestCase
from payonline.forms import PaymentDataForm


class PaymentDataFormTestCase(TestCase):

    def setUp(self):
        self.private_security_key = '123'

    def get_form_data(self):
        return {
            'DateTime': '2013-08-01 14:24:31',
            'TransactionID': '1',
            'OrderId': '125',
            'Amount': '125.00',
            'Currency': 'RUB',
            'Provider': 'Card',
            'SecurityKey': 'dc68debbb39ede71d786b2d49f40a9e8'
        }

    def test_form_valid(self):
        form = PaymentDataForm(
            data=self.get_form_data(),
            private_security_key=self.private_security_key
        )
        self.assertTrue(form.is_valid())

    def test_security_check(self):
        data = self.get_form_data()
        data['SecurityKey'] = 'dc68debbb39ede71d786b2d49f40a9e0'
        form = PaymentDataForm(
            data=data,
            private_security_key=self.private_security_key
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.non_field_errors()), 1)

    def test_unique_transaction(self):
        form = PaymentDataForm(
            data=self.get_form_data(),
            private_security_key=self.private_security_key
        )
        self.assertTrue(form.is_valid())
        form.save()
        form = PaymentDataForm(
            data=self.get_form_data(),
            private_security_key=self.private_security_key
        )
        self.assertFalse(form.is_valid())
