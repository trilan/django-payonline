from hashlib import md5

from django import forms
from django.utils.datastructures import SortedDict

from .models import PaymentData
from .helpers import DataProxy


class PaymentDataForm(forms.ModelForm):

    SecurityKey = forms.CharField(min_length=32, max_length=32)

    class Meta:
        model = PaymentData

    def __init__(self, *args, **kwargs):
        self.private_security_key = kwargs.pop('private_security_key', '')
        kwargs['data'] = DataProxy(kwargs['data'])
        super(PaymentDataForm, self).__init__(*args, **kwargs)

    def get_security_key_params(self):
        params = SortedDict()
        date_time = self.cleaned_data.get('datetime', '')
        if date_time:
            date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
        transaction_id = self.cleaned_data.get('transaction_id', '')
        order_id = self.cleaned_data.get('order_id', '')
        amount = self.cleaned_data.get('amount', '')
        params['DateTime'] = date_time
        params['TransactionID'] = str(transaction_id)
        params['OrderId'] = str(order_id)
        params['Amount'] = '%.2f' % amount if amount else ''
        params['Currency'] = self.cleaned_data.get('currency', '')
        params['PrivateSecurityKey'] = self.private_security_key
        return params

    def get_security_key(self):
        params = self.get_security_key_params()
        query_string = '&'.join('='.join(i) for i in params.items())
        key = md5(query_string).hexdigest()
        return key

    def clean(self):
        super(PaymentDataForm, self).clean()
        if self.cleaned_data.get('SecurityKey') != self.get_security_key():
            raise forms.ValidationError('Wrong security key')
        return self.cleaned_data
