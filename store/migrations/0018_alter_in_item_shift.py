# Generated by Django 5.0.7 on 2024-08-16 08:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_alter_in_item_shift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='in_item',
            name='shift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='store.shift'),
        ),
    ]
