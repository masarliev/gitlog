# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Project.private'
        db.delete_column('gitlog_project', 'private')

        # Deleting field 'Project.source'
        db.delete_column('gitlog_project', 'source')

        # Adding field 'Project.public'
        db.add_column('gitlog_project', 'public', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Project.url'
        db.add_column('gitlog_project', 'url', self.gf('django.db.models.fields.URLField')(max_length=30, null=True, blank=True), keep_default=False)

        # Adding field 'Project.description'
        db.add_column('gitlog_project', 'description', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding M2M table for field writable on 'Project'
        db.create_table('gitlog_project_writable', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['gitlog.project'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('gitlog_project_writable', ['project_id', 'user_id'])

        # Adding M2M table for field readonly on 'Project'
        db.create_table('gitlog_project_readonly', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['gitlog.project'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('gitlog_project_readonly', ['project_id', 'user_id'])

        # Changing field 'Project.owner'
        db.alter_column('gitlog_project', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))


    def backwards(self, orm):
        
        # Adding field 'Project.private'
        db.add_column('gitlog_project', 'private', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Project.source'
        db.add_column('gitlog_project', 'source', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'Project.public'
        db.delete_column('gitlog_project', 'public')

        # Deleting field 'Project.url'
        db.delete_column('gitlog_project', 'url')

        # Deleting field 'Project.description'
        db.delete_column('gitlog_project', 'description')

        # Removing M2M table for field writable on 'Project'
        db.delete_table('gitlog_project_writable')

        # Removing M2M table for field readonly on 'Project'
        db.delete_table('gitlog_project_readonly')

        # User chose to not deal with backwards NULL issues for 'Project.owner'
        raise RuntimeError("Cannot reverse this migration. 'Project.owner' and its values cannot be restored.")


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
        'gitlog.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owner'", 'null': 'True', 'to': "orm['auth.User']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'readonly': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'readonly'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'writable': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'writable'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['gitlog']
