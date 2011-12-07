from django.db import models
from .fields.models import UTCDateTimeField


CURRENCIES = (
    ('RUB', 'RUB'),
    ('USD', 'USD'),
    ('EUR', 'EUR'),
)

PROVIDERS = (
    ('Card', 'Card'),
    ('Qiwi', 'Qiwi'),
    ('WebMoney', 'WebMoney'),
)


class PaymentData(models.Model):

    datetime = UTCDateTimeField()
    transaction_id = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    provider = models.CharField(max_length=10, choices=PROVIDERS)

    card_holder = models.CharField(max_length=255, blank=True)
    card_number = models.CharField(max_length=16, blank=True)
    country = models.CharField(max_length=2, blank=True)
    city = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)

    wm_tran_id = models.PositiveIntegerField(null=True, blank=True)
    wm_inv_id = models.PositiveIntegerField(null=True, blank=True)
    wm_id = models.CharField(max_length=255, blank=True)
    wm_purse = models.CharField(max_length=255, blank=True)

    ip_address = models.CharField(max_length=255)
    ip_country = models.CharField(max_length=2)
    bin_country = models.CharField(max_length=2, blank=True)
