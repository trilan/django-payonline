import pytz
from hashlib import md5

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import SortedDict

from .models import PaymentData
from .helpers import DataProxy


class PaymentDataForm(forms.ModelForm):

    SecurityKey = forms.CharField(min_length=32, max_length=32)

    class Meta:
        model = PaymentData

    def __init__(self, *args, **kwargs):
        self.shop = kwargs.pop('shop')
        self.private_security_key = kwargs.pop('private_security_key')
        kwargs['data'] = DataProxy(kwargs['data'])
        super(PaymentDataForm, self).__init__(*args, **kwargs)

    def get_security_key_params(self):
        params = SortedDict()
        params['DateTime'] = self.data.get('DateTime', '')
        params['TransactionID'] = self.data.get('TransactionID', '')
        params['OrderId'] = self.data.get('OrderId', '')
        params['Amount'] = self.data.get('Amount', '')
        params['Currency'] = self.data.get('Currency', '')
        params['PrivateSecurityKey'] = self.private_security_key
        return params

    def get_security_key(self):
        params = self.get_security_key_params()
        key = md5('&'.join('='.join(i) for i in params.items())).hexdigest()
        return key

    def clean(self):
        if self.data.get('SecurityKey') != self.get_security_key():
            raise forms.ValidationError('Wrong security key')
        return self.cleaned_data
