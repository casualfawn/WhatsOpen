# Generated by Django 4.0.2 on 2024-12-17 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('woapi', '0003_rename_data_transformedcompanydata_company_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transformedcompanydata',
            name='close',
        ),
        migrations.RemoveField(
            model_name='transformedcompanydata',
            name='day',
        ),
        migrations.RemoveField(
            model_name='transformedcompanydata',
            name='open',
        ),
        migrations.RemoveField(
            model_name='transformedcompanydata',
            name='timestamp',
        ),
    ]
