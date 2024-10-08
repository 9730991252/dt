# Generated by Django 5.0.7 on 2024-08-02 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0004_batch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qr_code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_number', models.IntegerField(unique=True)),
                ('in_status', models.IntegerField(default=0)),
                ('out_status', models.IntegerField(default=0)),
                ('generate_date', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('batch', models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='office.batch')),
                ('employee', models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='office.employee')),
                ('product', models.ForeignKey(default=True, on_delete=django.db.models.deletion.PROTECT, to='office.product')),
            ],
        ),
    ]
