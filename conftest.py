#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django
from django.conf import settings

def pytest_configure():
    import sys

    try:
        import django  # NOQA
    except ImportError:
        print("Error: missing test dependency:")
        print("  django library is needed to run test suite")
        print("  you can install it with 'pip install django'")
        print("  or use tox to automatically handle test dependencies")
        sys.exit(1)

    try:
        import django_select2  # NOQA
    except ImportError:
        print("Error: missing test dependency:")
        print("  django_select2 library is needed to run test suite")
        print("  you can install it with 'pip install django_select2'")
        print("  or use tox to automatically handle test dependencies")
        sys.exit(1)

    try:
        import rarfile  # NOQA
    except ImportError:
        print("Error: missing test dependency:")
        print("  rarfile library is needed to run test suite")
        print("  you can install it with 'pip install rarfile'")
        print("  or use tox to automatically handle test dependencies")
        sys.exit(1)

    try:
        import suds  # NOQA
    except ImportError:
        print("Error: missing test dependency:")
        print("  suds library is needed to run test suite")
        print("  you can install it with 'pip install suds'")
        print("  or use tox to automatically handle test dependencies")
        sys.exit(1)

    try:
        import six  # NOQA
    except ImportError:
        print("Error: missing test dependency:")
        print("  six library is needed to run test suite")
        print("  you can install it with 'pip install six'")
        print("  or use tox to automatically handle test dependencies")
        sys.exit(1)

    settings.configure(
        INSTALLED_APPS=[
            'tests.testapp',
            'fias',
        ],
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite',
            },
            'fias': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'fias_test',
                'USER': 'postgres',
                'PASSWORD': '',
                'HOST': '127.0.0.1',
                'PORT': '5432',
            },
        },
        SECRET_KEY='key',
        FIAS_DATABASE_ALIAS='fias',
        DATABASE_ROUTERS=['fias.routers.FIASRouter'],
        ROOT_URLCONF='tests.urls',
        DEBUG=True,
        TEMPLATE_DEBUG=True,

    )
