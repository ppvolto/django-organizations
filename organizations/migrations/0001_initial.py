# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import organizations.fields
import organizations.base
import django.utils.timezone
from django.conf import settings

from organizations.settings import organizations_settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(organizations_settings.ORGANIZATION_MODEL),
        migrations.swappable_dependency(organizations_settings.ORGANIZATION_USER_MODEL),
        migrations.swappable_dependency(organizations_settings.ORGANIZATION_OWNER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name of the organization', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('created', organizations.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', organizations.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('slug', organizations.fields.SlugField(populate_from=b'name', editable=True, max_length=200, help_text='The name in all lowercase, suitable for URL identification', unique=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'swappable': 'DJANGO_ORGANIZATION_ORGANIZATION_MODEL',
                'verbose_name': 'organization',
                'verbose_name_plural': 'organizations',
            }
        ),
        migrations.CreateModel(
            name='OrganizationOwner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', organizations.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', organizations.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('organization', models.OneToOneField(related_name='owner', to=organizations_settings.ORGANIZATION_MODEL)),
            ],
            options={
                'swappable': 'DJANGO_ORGANIZATION_ORGANIZATION_OWNER_MODEL',
                'verbose_name': 'organization owner',
                'verbose_name_plural': 'organization owners',
            }
        ),
        migrations.CreateModel(
            name='OrganizationUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', organizations.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', organizations.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(related_name='organization_users', to=organizations_settings.ORGANIZATION_MODEL)),
                ('user', models.ForeignKey(related_name='organizations_organizationuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['organization', 'user'],
                'abstract': False,
                'swappable': 'DJANGO_ORGANIZATION_ORGANIZATION_USER_MODEL',
                'verbose_name': 'organization user',
                'verbose_name_plural': 'organization users',
            }
        ),
        migrations.AddField(
            model_name='organizationowner',
            name='organization_user',
            field=models.OneToOneField(to=organizations_settings.ORGANIZATION_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organization',
            name='users',
            field=models.ManyToManyField(related_name='organizations_organization', through=organizations_settings.ORGANIZATION_USER_MODEL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='organizationuser',
            unique_together=set([('user', 'organization')]),
        ),
    ]
