Django PayOnline
================

Django PayOnline is an application for integration with `PayOnline System`_.

Installation
------------

Install django-payonline with pip::

    pip install django-payonline

Configuration
-------------

1. Add ``payonline`` app to ``INSTALLED_APPS``::

       INSTALLED_APPS = (
           ...
           'payonline',
       )

2. Run ``syncdb`` command (with ``--migrate`` flag if you use South).

3. Set app config in project's settings::

       PAYONLINE_CONFIG = {
           'MERCHANT_ID': '...',
           'PRIVATE_SECURITY_KEY': '...',
       }

4. Add ``payonline.urls`` to project's urlconf::

       urlpatterns = patterns(
           ...
           url(r'^payonline/', include('payonline.urls')),
       )

Contributing
------------

Feel free to fork, send pull requests or report bugs and issues on github.

.. _Payonline System: http://www.payonlinesystem.com/
