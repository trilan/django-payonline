import urllib
from decimal import Decimal, InvalidOperation
from hashlib import md5

from django.http import (HttpResponseBadRequest,
                         HttpResponseRedirect,
                         HttpResponse)
from django.shortcuts import render
from django.utils.datastructures import SortedDict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.core.urlresolvers import reverse

from sitesutils.helpers import get_site

from .forms import PaymentDataForm
from .loader import get_success_backends, get_fail_backends
from .settings import CONFIG


class PayView(View):

    def get_order_id(self):
        return unicode(self.request.session.get('payonline_order_id', ''))

    def get_amount(self):
        amount = self.request.session.get('payonline_amount', 0)
        try:
            amount = Decimal(amount)
        except InvalidOperation:
            return '0.00'
        return u'{0:.2f}'.format(amount)

    def get_merchant_id(self):
        return CONFIG['MERCHANT_ID']

    def get_currency(self):
        return CONFIG['CURRENCY']

    def get_private_security_key(self):
        return CONFIG['PRIVATE_SECURITY_KEY']

    def get_payonline_url(self):
        return CONFIG['PAYONLINE_URL']

    def get_fail_url(self):
        site = get_site(self.request)
        return 'http://%s%s' % (site.domain, reverse('payonline_fail'))

    def get_return_url(self):
        site = get_site(self.request)
        return_url = self.request.session.get('payonline_return_url')
        return_url = return_url or reverse('payonline_success')
        return 'http://%s%s' % (site.domain, return_url)

    def get_security_key_params(self):
        params = SortedDict()
        params['MerchantId'] = self.get_merchant_id()
        params['OrderId'] = self.get_order_id()
        params['Amount'] = self.get_amount()
        params['Currency'] = self.get_currency()
        params['PrivateSecurityKey'] = self.get_private_security_key()
        return params

    def get_security_key(self):
        params = self.get_security_key_params()
        return md5(urllib.urlencode(params)).hexdigest()

    def get_query_params(self):
        params = {'MerchantId': self.get_merchant_id(),
                  'OrderId': self.get_order_id(),
                  'Amount': self.get_amount(),
                  'Currency': self.get_currency(),
                  'SecurityKey': self.get_security_key(),
                  'FailUrl': self.get_fail_url(),
                  'ReturnUrl': self.get_return_url()}
        return params

    def get_redirect_url(self):
        params = self.get_query_params()
        redirect_url = self.get_payonline_url() + '?'
        query_string = urllib.urlencode(params)
        redirect_url += query_string
        return redirect_url

    def get(self, request, *args, **kwargs):
        if self.get_order_id():
            redirect_url = self.get_redirect_url()
            return HttpResponseRedirect(redirect_url)
        return HttpResponseBadRequest()


class CallbackView(View):

    def get_private_security_key(self):
        return CONFIG['PRIVATE_SECURITY_KEY']

    def get_form(self, data):
        return PaymentDataForm(
            data=data, private_security_key=self.get_private_security_key()
        )

    def process_form(self, form):
        if form.is_valid():
            payment_data = form.save()
            backends = get_success_backends()
            for backend in backends:
                backend(payment_data)
            return HttpResponse()
        return HttpResponseBadRequest()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CallbackView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.process_form(self.get_form(request.GET))

    def post(self, request, *args, **kwargs):
        return self.process_form(self.get_form(request.POST))


class FailView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(FailView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'ErrorCode' not in request.POST:
            return HttpResponseBadRequest()
        backends = get_fail_backends()
        for backend in backends:
            backend(request, request.POST['ErrorCode'])
        return render(request, 'payonline/fail.html', {
            'error_code': request.POST['ErrorCode'],
        })


class SuccessView(View):

    def get_context_data(self, **kwargs):
        return kwargs

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data()
        return render(request, 'payonline/success.html', context_data)
