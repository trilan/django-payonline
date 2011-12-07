import os
import sys

from django.conf import settings
from django.template.loader import BaseLoader


if not settings.configured:
    settings.configure(
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        LANGUAGE_CODE = 'ru',
        LANGUAGES = (
            ('ru', 'Russian'),
            ('en', 'English'),
        ),
        INSTALLED_APPS = (
            'lemon.extradmin',

            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.messages',
            'django.contrib.sessions',
            'django.contrib.sites',

            'lemon.filebrowser',
            'lemon.metatags',
            'lemon.publications',

            'intellipages',
            'utils',
            'shop',
            'shop_simple',
            'payonline',
        ),
        SITE_ID = 1,
        STATIC_URL = 'static',
        ROOT_URLCONF = '',
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'lemon.utils.middleware.sites.RequestSiteMiddleware',
        ),
    )


def main():
    from django.test.utils import get_runner

    test_runner = get_runner(settings)(interactive=False)
    failures = test_runner.run_tests(['payonline'])
    sys.exit(failures)


if __name__ == '__main__':
    main()
