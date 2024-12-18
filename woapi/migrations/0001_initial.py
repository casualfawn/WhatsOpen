# Generated by Django 4.0.2 on 2024-12-17 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TransformedCompanyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50)),
                ('days_open', models.SmallIntegerField()),
                ('hours_open', models.CharField(max_length=100)),
            ],
        ),
    ]
