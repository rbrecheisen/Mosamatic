# Generated by Django 5.1.7 on 2025-04-07 06:26

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LogOutputModel',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('_mode', models.CharField(choices=[('info', 'info'), ('warning', 'warning'), ('error', 'error')], default='info', editable=False, max_length=8)),
                ('_timestamp', models.DateTimeField(auto_now_add=True)),
                ('_message', models.CharField(editable=False, max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='FileSetModel',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('_name', models.CharField(max_length=1024)),
                ('_path', models.CharField(editable=False, max_length=2048, null=True, unique=True)),
                ('_created', models.DateTimeField(auto_now_add=True)),
                ('_owner', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('_name', models.CharField(editable=False, max_length=256)),
                ('_path', models.CharField(editable=False, max_length=2048)),
                ('_fileset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.filesetmodel')),
            ],
        ),
    ]
