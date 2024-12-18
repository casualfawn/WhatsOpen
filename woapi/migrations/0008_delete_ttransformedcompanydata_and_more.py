# Generated by Django 4.0.2 on 2024-12-17 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woapi', '0007_ttransformedcompanydata'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TTransformedCompanyData',
        ),
        migrations.RemoveField(
            model_name='transformedcompanydata',
            name='company_name',
        ),
        migrations.AddField(
            model_name='transformedcompanydata',
            name='data',
            field=models.TextField(default='hi'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transformedcompanydata',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default='2024-01-01 00:00:00'),
            preserve_default=False,
        ),
    ]
