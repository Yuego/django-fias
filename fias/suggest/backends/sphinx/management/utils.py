# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connections
from django.template import Context
from django.template.loader import select_template

from fias.compat import TemplateDoesNotExist
from fias.config import DATABASE_ALIAS
from ..config import SPHINX_ADDROBJ_INDEX
import re

connection = connections[DATABASE_ALIAS]

def _get_database_engine():
    _engine = connection.vendor

    if 'mysql' in _engine:
        return 'mysql'
    elif 'postgresql' in _engine or 'postgis' in _engine:
        return 'pgsql'

    raise ImproperlyConfigured("Only MySQL and PostgreSQL, and PostGIS engines are supported by FIAS.")


def _get_template(name):
    return select_template(['fias/sphinx/' + name])


def _get_sql_template(name):
    return _get_template('sql/{0}/{1}.sql'.format(_get_database_engine(), name))


def _get_sphinx_template(name):
    return _get_template('config/{0}.conf'.format(name))

try:
    _get_sql_template('query')
except TemplateDoesNotExist:
    raise ImproperlyConfigured('FIAS: database backend `{0}` '
                               'is not supported with `sphinx` suggest backend!'.format(connection.vendor))


def render_sphinx_source():

    ctx = {
        'db_type': _get_database_engine(),
        'db_host': settings.DATABASES[DATABASE_ALIAS]['HOST'],
        'db_port': settings.DATABASES[DATABASE_ALIAS]['PORT'],
        'db_name': settings.DATABASES[DATABASE_ALIAS]['NAME'],
        'db_user': settings.DATABASES[DATABASE_ALIAS]['USER'],
        'db_password': settings.DATABASES[DATABASE_ALIAS]['PASSWORD'],

        'index_name': SPHINX_ADDROBJ_INDEX,
    }

    re_nl = re.compile(r'(?<!;)\n', re.U)
    re_strip_el = re.compile(r'^\n', re.MULTILINE)
    for query_type in ['_pre', '_post', '']:
        query_name = 'query' + query_type
        query = _get_sql_template(query_name).render(Context({}))
        ctx['db_' + query_name] = re_nl.sub(r'\\\n', re_strip_el.sub('', query)).strip()

    return _get_sphinx_template('source').render(Context(ctx))


def render_sphinx_index(path):
    ctx = {
        'sphinx_index_path': path,

        'index_name': SPHINX_ADDROBJ_INDEX,
    }

    return _get_sphinx_template('index').render(Context(ctx))


def render_sphinx_config(path, full=True):
    source = render_sphinx_source()
    index = render_sphinx_index(path)

    config = _get_sphinx_template('sphinx').render(Context({})) if full else ''

    return source, index, config
