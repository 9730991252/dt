# Generated by Django 5.0.7 on 2024-08-08 04:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0007_rename_product_item_rename_product_batch_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qr_code',
            name='batch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='office.batch'),
        ),
        migrations.AlterField(
            model_name='qr_code',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='office.employee'),
        ),
        migrations.AlterField(
            model_name='qr_code',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='office.item'),
        ),
    ]
