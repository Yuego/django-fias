from .settings import *


DATABASES['fias'] = {
    {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'fias_test',
       'USER': 'postgres',
       'PASSWORD': '',
       'HOST': '127.0.0.1',
       'PORT': '5432',
    },
}

FIAS_DATABASE_ALIAS = 'fias'
DATABASE_ROUTERS = ['fias.routers.FIASRouter']
