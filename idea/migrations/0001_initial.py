# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IdeaCategory'
        db.create_table('idea_ideacategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('idea', ['IdeaCategory'])

        # Adding model 'IdeaImage'
        db.create_table('idea_ideaimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('idea', ['IdeaImage'])

        # Adding model 'Idea'
        db.create_table('idea_idea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['idea.IdeaCategory'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('vote_yes_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('vote_no_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('idea', ['Idea'])

        # Adding M2M table for field images on 'Idea'
        db.create_table('idea_idea_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idea', models.ForeignKey(orm['idea.idea'], null=False)),
            ('ideaimage', models.ForeignKey(orm['idea.ideaimage'], null=False))
        ))
        db.create_unique('idea_idea_images', ['idea_id', 'ideaimage_id'])

        # Adding model 'IdeaVote'
        db.create_table('idea_ideavote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('idea', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['idea.Idea'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('state', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('idea', ['IdeaVote'])

        # Adding unique constraint on 'IdeaVote', fields ['idea', 'user']
        db.create_unique('idea_ideavote', ['idea_id', 'user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'IdeaVote', fields ['idea', 'user']
        db.delete_unique('idea_ideavote', ['idea_id', 'user_id'])

        # Deleting model 'IdeaCategory'
        db.delete_table('idea_ideacategory')

        # Deleting model 'IdeaImage'
        db.delete_table('idea_ideaimage')

        # Deleting model 'Idea'
        db.delete_table('idea_idea')

        # Removing M2M table for field images on 'Idea'
        db.delete_table('idea_idea_images')

        # Deleting model 'IdeaVote'
        db.delete_table('idea_ideavote')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'idea.idea': {
            'Meta': {'object_name': 'Idea'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['idea.IdeaCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['idea.IdeaImage']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'vote_no_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vote_yes_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'idea.ideacategory': {
            'Meta': {'object_name': 'IdeaCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'idea.ideaimage': {
            'Meta': {'object_name': 'IdeaImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'idea.ideavote': {
            'Meta': {'unique_together': "(('idea', 'user'),)", 'object_name': 'IdeaVote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['idea.Idea']"}),
            'state': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['idea']