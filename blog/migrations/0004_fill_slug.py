# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from blog.models import BlogHolder

class Migration(DataMigration):

    def forwards(self, orm):
        for el in BlogHolder.objects.all():
            el.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'blog.blogentry': {
            'Meta': {'ordering': "['-date']", 'object_name': 'BlogEntry'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'holder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['blog.BlogHolder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'blog.blogholder': {
            'Meta': {'object_name': 'BlogHolder'},
            'autor_about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'autor_contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'autor_contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'autor_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'autor_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'district': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['blog']
    symmetrical = True
