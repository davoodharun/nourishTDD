# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fridges', '0002_storage_text'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Storage',
            new_name='Store',
        ),
    ]
