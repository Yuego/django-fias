# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'House.oktmo'
        db.alter_column(u'fias_house', 'oktmo', self.gf('django.db.models.fields.BigIntegerField')(null=True))

        # Changing field 'AddrObj.oktmo'
        db.alter_column(u'fias_addrobj', 'oktmo', self.gf('django.db.models.fields.BigIntegerField')(null=True))

        # Changing field 'LandMark.oktmo'
        db.alter_column(u'fias_landmark', 'oktmo', self.gf('django.db.models.fields.BigIntegerField')(null=True))

        # Changing field 'HouseInt.oktmo'
        db.alter_column(u'fias_houseint', 'oktmo', self.gf('django.db.models.fields.BigIntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'House.oktmo'
        db.alter_column(u'fias_house', 'oktmo', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'AddrObj.oktmo'
        db.alter_column(u'fias_addrobj', 'oktmo', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'LandMark.oktmo'
        db.alter_column(u'fias_landmark', 'oktmo', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'HouseInt.oktmo'
        db.alter_column(u'fias_houseint', 'oktmo', self.gf('django.db.models.fields.IntegerField')(null=True))

    models = {
        u'fias.addrobj': {
            'Meta': {'ordering': "[u'aolevel', u'formalname']", 'object_name': 'AddrObj', 'index_together': "((u'aolevel', u'shortname'), (u'shortname', u'formalname'))"},
            'actstatus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'aoguid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'aoid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36', 'blank': 'True'}),
            'aolevel': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'}),
            'areacode': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'autocode': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'centstatus': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'citycode': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'ctarcode': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'currstatus': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'extrcode': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'formalname': ('django.db.models.fields.CharField', [], {'max_length': '120', 'db_index': 'True'}),
            'formalname_en': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'formalname_ru': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'formalname_uk': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'ifnsfl': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ifnsul': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'livestatus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nextid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'normdoc': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'offname': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'okato': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'oktmo': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'operstatus': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'parentguid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'placecode': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'plaincode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'postalcode': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'previd': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'regioncode': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'sextcode': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'shortname_en': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'shortname_ru': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'shortname_uk': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'startdate': ('django.db.models.fields.DateField', [], {}),
            'streetcode': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'terrifnsfl': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'terrifnsul': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updatedate': ('django.db.models.fields.DateField', [], {})
        },
        u'fias.addrobjindex': {
            'Meta': {'object_name': 'AddrObjIndex'},
            'aoguid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'aolevel': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'fullname': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_weight': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '64'}),
            'scname': ('django.db.models.fields.TextField', [], {})
        },
        u'fias.house': {
            'Meta': {'object_name': 'House'},
            'aoguid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fias.AddrObj']"}),
            'buildnum': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'counter': ('django.db.models.fields.IntegerField', [], {}),
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'eststatus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'houseguid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'houseid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'housenum': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'ifnsfl': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ifnsul': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'normdoc': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'okato': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'oktmo': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'postalcode': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'startdate': ('django.db.models.fields.DateField', [], {}),
            'statstatus': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'strstatus': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'strucnum': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'terrifnsfl': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'terrifnsul': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updatedate': ('django.db.models.fields.DateField', [], {})
        },
        u'fias.houseint': {
            'Meta': {'object_name': 'HouseInt'},
            'aoguid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fias.AddrObj']"}),
            'counter': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'houseintid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'ifnsfl': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ifnsul': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'intend': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intguid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'intstart': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intstatus': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'normdoc': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'okato': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'oktmo': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'postalcode': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'startdate': ('django.db.models.fields.DateField', [], {}),
            'terrifnsfl': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'terrifnsul': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updatedate': ('django.db.models.fields.DateField', [], {})
        },
        u'fias.landmark': {
            'Meta': {'object_name': 'LandMark'},
            'aoguid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fias.AddrObj']"}),
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'ifnsfl': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ifnsul': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'landguid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'landid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'normdoc': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'okato': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'oktmo': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'postalcode': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'startdate': ('django.db.models.fields.DateField', [], {}),
            'terrifnsfl': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'terrifnsul': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updatedate': ('django.db.models.fields.DateField', [], {})
        },
        u'fias.normdoc': {
            'Meta': {'object_name': 'NormDoc'},
            'docdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'docimgid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'docname': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'docnum': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'doctype': ('django.db.models.fields.IntegerField', [], {}),
            'normdocid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        u'fias.socrbase': {
            'Meta': {'ordering': "[u'level', u'scname']", 'object_name': 'SocrBase', 'index_together': "((u'level', u'scname'),)"},
            'item_weight': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '64'}),
            'kod_t_st': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'scname': ('django.db.models.fields.CharField', [], {'default': "u' '", 'max_length': '10'}),
            'scname_en': ('django.db.models.fields.CharField', [], {'default': "u' '", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'scname_ru': ('django.db.models.fields.CharField', [], {'default': "u' '", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'scname_uk': ('django.db.models.fields.CharField', [], {'default': "u' '", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'socrname': ('django.db.models.fields.CharField', [], {'default': "u' '", 'max_length': '50'}),
            'socrname_en': ('django.db.models.fields.CharField', [], {'default': "u' '", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'socrname_ru': ('django.db.models.fields.CharField', [], {'default': "u' '", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'socrname_uk': ('django.db.models.fields.CharField', [], {'default': "u' '", 'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'fias.status': {
            'Meta': {'object_name': 'Status'},
            'table': ('django.db.models.fields.CharField', [], {'max_length': '15', 'primary_key': 'True'}),
            'ver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fias.Version']"})
        },
        u'fias.version': {
            'Meta': {'object_name': 'Version'},
            'complete_xml_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'delta_xml_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dumpdate': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'ver': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['fias']