# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fridges', '0005_item_store'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Store',
            new_name='Fridge',
        ),
    ]
