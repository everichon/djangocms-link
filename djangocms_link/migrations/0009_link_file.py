# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0004_auto_20160328_1434'),
        ('djangocms_link', '0008_auto_20160522_0203'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='file',
            field=filer.fields.file.FilerFileField(related_name='link_file', on_delete=django.db.models.deletion.SET_NULL, verbose_name='File Link', blank=True, to='filer.File', null=True),
        ),
    ]
