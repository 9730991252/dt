# Generated by Django 5.0.7 on 2024-08-03 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0007_rename_product_item_rename_product_batch_item_and_more'),
        ('store', '0002_in_stock_scan_type_alter_in_stock_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='In_stock',
            new_name='In_item',
        ),
    ]
