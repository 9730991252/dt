# Generated by Django 5.0.7 on 2024-08-25 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0021_machine_working_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='mobile',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='employee',
            name='pin',
            field=models.IntegerField(),
        ),
    ]
