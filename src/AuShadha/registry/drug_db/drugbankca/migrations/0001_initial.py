# Generated by Django 2.1 on 2018-09-11 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DrugBankCaDrugs',
            fields=[
                ('drug_name', models.TextField(max_length=1000, primary_key=True, serialize=False, verbose_name='Drug Name')),
                ('drug_id', models.CharField(max_length=30, verbose_name='Drug-ID')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
