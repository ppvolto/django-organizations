# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from organizations.settings import organizations_settings
from organizations.fields import SlugField

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(organizations_settings.ORGANIZATION_SLUGFIELD),
    ]

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=SlugField(help_text='The name in all lowercase, suitable for URL identification', unique=True, populate_from='name', max_length=200, editable=True),
        ),
    ]
