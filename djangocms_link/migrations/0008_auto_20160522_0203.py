# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0014_auto_20160404_1908'),
        ('djangocms_link', '0007_set_related_name_for_cmsplugin_ptr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='page_link',
        ),
        migrations.AddField(
            model_name='link',
            name='page',
            field=cms.models.fields.PageField(blank=True, to='cms.Page', null=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.URLField(help_text='If page is not set, you can enter a link here.', max_length=255, null=True, blank=True),
        ),
    ]
