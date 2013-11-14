# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Version'
        db.create_table(u'fias_version', (
            ('ver', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(db_index=True, null=True, blank=True)),
            ('dumpdate', self.gf('django.db.models.fields.DateField')(db_index=True)),
        ))
        db.send_create_signal(u'fias', ['Version'])

        # Adding model 'Status'
        db.create_table(u'fias_status', (
            ('table', self.gf('django.db.models.fields.CharField')(max_length=15, primary_key=True)),
            ('ver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fias.Version'])),
        ))
        db.send_create_signal(u'fias', ['Status'])

        # Adding model 'SocrBase'
        db.create_table(u'fias_socrbase', (
            ('level', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('scname', self.gf('django.db.models.fields.CharField')(default=u' ', max_length=10)),
            ('socrname', self.gf('django.db.models.fields.CharField')(default=u' ', max_length=50)),
            ('kod_t_st', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
        ))
        db.send_create_signal(u'fias', ['SocrBase'])

        # Adding index on 'SocrBase', fields ['level', 'scname']
        db.create_index(u'fias_socrbase', ['level', 'scname'])

        # Adding model 'NormDoc'
        db.create_table(u'fias_normdoc', (
            ('normdocid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('docname', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('docdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('docnum', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('doctype', self.gf('django.db.models.fields.IntegerField')()),
            ('docimgid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'fias', ['NormDoc'])

        # Adding model 'AddrObj'
        db.create_table(u'fias_addrobj', (
            ('ifnsfl', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('terrifnsfl', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('ifnsul', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('terrifnsul', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('okato', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('oktmo', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('postalcode', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('updatedate', self.gf('django.db.models.fields.DateField')()),
            ('startdate', self.gf('django.db.models.fields.DateField')()),
            ('enddate', self.gf('django.db.models.fields.DateField')()),
            ('normdoc', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('aoguid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('parentguid', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=36, null=True, blank=True)),
            ('aoid', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=36, blank=True)),
            ('previd', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('nextid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('formalname', self.gf('django.db.models.fields.CharField')(max_length=120, db_index=True)),
            ('offname', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('shortname', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
            ('aolevel', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True)),
            ('regioncode', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('autocode', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('areacode', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('citycode', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('ctarcode', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('placecode', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('streetcode', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('extrcode', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('sextcode', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=17, null=True, blank=True)),
            ('plaincode', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('actstatus', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('centstatus', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('operstatus', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('currstatus', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('livestatus', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'fias', ['AddrObj'])

        # Adding index on 'AddrObj', fields ['aolevel', 'shortname']
        db.create_index(u'fias_addrobj', ['aolevel', 'shortname'])

        # Adding index on 'AddrObj', fields ['shortname', 'formalname']
        db.create_index(u'fias_addrobj', ['shortname', 'formalname'])

        # Adding model 'House'
        db.create_table(u'fias_house', (
            ('ifnsfl', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('terrifnsfl', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('ifnsul', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('terrifnsul', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('okato', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('oktmo', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('postalcode', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('updatedate', self.gf('django.db.models.fields.DateField')()),
            ('startdate', self.gf('django.db.models.fields.DateField')()),
            ('enddate', self.gf('django.db.models.fields.DateField')()),
            ('normdoc', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('aoguid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fias.AddrObj'])),
            ('housenum', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('eststatus', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('buildnum', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('strucnum', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('strstatus', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('houseguid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('houseid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('statstatus', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('counter', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'fias', ['House'])

        # Adding model 'HouseInt'
        db.create_table(u'fias_houseint', (
            ('ifnsfl', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('terrifnsfl', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('ifnsul', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('terrifnsul', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('okato', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('oktmo', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('postalcode', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('updatedate', self.gf('django.db.models.fields.DateField')()),
            ('startdate', self.gf('django.db.models.fields.DateField')()),
            ('enddate', self.gf('django.db.models.fields.DateField')()),
            ('normdoc', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('houseintid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('intguid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('aoguid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fias.AddrObj'])),
            ('intstart', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('intend', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('intstatus', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('counter', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'fias', ['HouseInt'])

        # Adding model 'LandMark'
        db.create_table(u'fias_landmark', (
            ('ifnsfl', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('terrifnsfl', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('ifnsul', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('terrifnsul', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('okato', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('oktmo', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('postalcode', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('updatedate', self.gf('django.db.models.fields.DateField')()),
            ('startdate', self.gf('django.db.models.fields.DateField')()),
            ('enddate', self.gf('django.db.models.fields.DateField')()),
            ('normdoc', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('landid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('landguid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('aoguid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fias.AddrObj'])),
            ('location', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'fias', ['LandMark'])


    def backwards(self, orm):
        # Removing index on 'AddrObj', fields ['shortname', 'formalname']
        db.delete_index(u'fias_addrobj', ['shortname', 'formalname'])

        # Removing index on 'AddrObj', fields ['aolevel', 'shortname']
        db.delete_index(u'fias_addrobj', ['aolevel', 'shortname'])

        # Removing index on 'SocrBase', fields ['level', 'scname']
        db.delete_index(u'fias_socrbase', ['level', 'scname'])

        # Deleting model 'Version'
        db.delete_table(u'fias_version')

        # Deleting model 'Status'
        db.delete_table(u'fias_status')

        # Deleting model 'SocrBase'
        db.delete_table(u'fias_socrbase')

        # Deleting model 'NormDoc'
        db.delete_table(u'fias_normdoc')

        # Deleting model 'AddrObj'
        db.delete_table(u'fias_addrobj')

        # Deleting model 'House'
        db.delete_table(u'fias_house')

        # Deleting model 'HouseInt'
        db.delete_table(u'fias_houseint')

        # Deleting model 'LandMark'
        db.delete_table(u'fias_landmark')


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
            'ifnsfl': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ifnsul': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'livestatus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nextid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'normdoc': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'offname': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'okato': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'oktmo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'operstatus': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'parentguid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'placecode': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'plaincode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'postalcode': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'previd': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'regioncode': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'sextcode': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'startdate': ('django.db.models.fields.DateField', [], {}),
            'streetcode': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'terrifnsfl': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'terrifnsul': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updatedate': ('django.db.models.fields.DateField', [], {})
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
            'oktmo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'oktmo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'oktmo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'kod_t_st': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'scname': ('django.db.models.fields.CharField', [], {'default': "u' '", 'max_length': '10'}),
            'socrname': ('django.db.models.fields.CharField', [], {'default': "u' '", 'max_length': '50'})
        },
        u'fias.status': {
            'Meta': {'object_name': 'Status'},
            'table': ('django.db.models.fields.CharField', [], {'max_length': '15', 'primary_key': 'True'}),
            'ver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fias.Version']"})
        },
        u'fias.version': {
            'Meta': {'object_name': 'Version'},
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'dumpdate': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'ver': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['fias']