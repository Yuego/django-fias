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
        import zeep  # NOQA
    except ImportError:
        print("Error: missing test dependency:")
        print("  zeep library is needed to run test suite")
        print("  you can install it with 'pip install zeep'")
        print("  or use tox to automatically handle test dependencies")
        sys.exit(1)

    try:
        import dbfread  # NOQA
    except ImportError:
        print("Error: missing test dependency:")
        print("  dbfread library is needed to run test suite")
        print("  you can install it with 'pip install dbfread'")
        print("  or use tox to automatically handle test dependencies")
        sys.exit(1)

    try:
        import progress  # NOQA
    except ImportError:
        print("Error: missing test dependency:")
        print("  progress library is needed to run test suite")
        print("  you can install it with 'pip install progress'")
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
            'fias',
        ],
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite',
            },
            'fias': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'fias.sqlite',
            },
        },
        SECRET_KEY='key',
        ROOT_URLCONF='tests.urls',
        FIAS_DATABASE_ALIAS='fias',
        DATABASE_ROUTERS=['fias.routers.FIASRouter'],
        DEBUG=True,
        TEMPLATE_DEBUG=True,

    )
