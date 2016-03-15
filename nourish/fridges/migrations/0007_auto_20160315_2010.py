# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fridges', '0006_auto_20160315_2006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='store',
            new_name='fridge',
        ),
    ]
