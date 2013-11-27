#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db.utils import DEFAULT_DB_ALIAS

from fias.config import FIAS_DATABASE_ALIAS


class FIASRouter(object):
    ALLOWED_REL = ['AddrObj']
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'fias':
            return FIAS_DATABASE_ALIAS
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'fias':
            return FIAS_DATABASE_ALIAS
        else:
            """\
            Странный хак, но без него
            джанго не может правильно определить БД для записи\
            """
            try:
                if hints['instance']._meta.object_name == 'AddrObj':
                    return DEFAULT_DB_ALIAS
            except KeyError:
                pass
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """\
        Разрешить связи из других бд к таблицам ФИАС
        но запретить ссылаться из бд ФИАС в другие БД
        """

        if obj1._meta.app_label == 'fias' and obj2._meta.app_label == 'fias':
            return True
        elif obj1._meta.app_label == 'fias' and obj1._meta.object_name in self.ALLOWED_REL:
            return True
        return None

    def allow_syncdb(self, db, model):
        """Разрешить синхронизацию моделей в базе ФИАС"""
        if db == FIAS_DATABASE_ALIAS:
            if model._meta.app_label in ('fias', 'south'):
                return True
            else:
                return False
        elif model._meta.app_label == 'fias':
            return False

        return None
