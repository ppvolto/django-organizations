# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 13:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import organizations.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleOrganization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the organization', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('custom_field', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SampleOrganizationOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_field', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SampleOrganizationUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_field', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['organization', 'user'],
                'abstract': False,
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('sampleorganization_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='test_custom.SampleOrganization')),
                ('sport', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=('test_custom.sampleorganization',),
        ),
        migrations.AddField(
            model_name='sampleorganizationuser',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_users', to='test_custom.SampleOrganization'),
        ),
        migrations.AddField(
            model_name='sampleorganizationuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_custom_sampleorganizationuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sampleorganizationowner',
            name='organization',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='test_custom.SampleOrganization'),
        ),
        migrations.AddField(
            model_name='sampleorganizationowner',
            name='organization_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='test_custom.SampleOrganizationUser'),
        ),
        migrations.AddField(
            model_name='sampleorganization',
            name='users',
            field=models.ManyToManyField(related_name='test_custom_sampleorganization', through='test_custom.SampleOrganizationUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='sampleorganizationuser',
            unique_together=set([('user', 'organization')]),
        ),
    ]
