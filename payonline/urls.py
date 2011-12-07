from django.conf.urls.defaults import patterns, url
from .views import PayView, CallbackView, FailView, SuccessView


urlpatterns = patterns(
    '',
    url(r'^$', PayView.as_view(), name='payonline_pay'),
    url(r'^callback/$', CallbackView.as_view(), name='payonline_callback'),
    url(r'^fail/$', FailView.as_view(), name='payonline_fail'),
    url(r'^success/$', SuccessView.as_view(), name='payonline_success'),
)
