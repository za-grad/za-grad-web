# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BlogHolder'
        db.create_table('blog_blogholder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('district', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('autor_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('autor_contact', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('autor_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('autor_about', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('blog', ['BlogHolder'])

        # Adding model 'BlogEntry'
        db.create_table('blog_blogentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('holder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.BlogHolder'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('blog', ['BlogEntry'])


    def backwards(self, orm):
        # Deleting model 'BlogHolder'
        db.delete_table('blog_blogholder')

        # Deleting model 'BlogEntry'
        db.delete_table('blog_blogentry')


    models = {
        'blog.blogentry': {
            'Meta': {'object_name': 'BlogEntry'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'holder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.BlogHolder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'blog.blogholder': {
            'Meta': {'object_name': 'BlogHolder'},
            'autor_about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'autor_contact': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'autor_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'autor_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'district': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['blog']