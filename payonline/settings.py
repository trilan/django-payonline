from django.conf import settings


CONFIG = {
    'MERCHANT_ID': None,
    'PRIVATE_SECURITY_KEY': None,
    'PAYONLINE_URL': 'https://secure.payonlinesystem.com/ru/payment/select/',
    'CURRENCY': 'RUB',
}
CONFIG.update(getattr(settings, 'PAYONLINE_CONFIG', {}))
