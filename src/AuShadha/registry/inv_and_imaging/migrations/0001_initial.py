# Generated by Django 2.1 on 2018-09-11 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImagingInvestigationRegistry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modality', models.CharField(max_length=30)),
                ('area_studied', models.CharField(max_length=30)),
                ('remarks', models.TextField(default='NAD', help_text='limit to 200 words', max_length=200)),
            ],
            options={
                'verbose_name': 'Imaging Investigation Registry',
                'verbose_name_plural': 'Imaging Investigation Registry',
            },
        ),
        migrations.CreateModel(
            name='LabInvestigationRegistry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_investigation', models.CharField(max_length=30, unique=True)),
                ('lower_limit', models.DecimalField(decimal_places=2, default=0, max_digits=7, max_length=10)),
                ('higher_limit', models.DecimalField(decimal_places=2, default=0, max_digits=7, max_length=10)),
                ('unit', models.CharField(blank=True, max_length=20, null=True)),
                ('method', models.CharField(blank=True, max_length=30, null=True)),
                ('analyser', models.CharField(blank=True, max_length=30, null=True)),
                ('remarks', models.TextField(default='NAD', help_text='limit to 200 words', max_length=200)),
            ],
            options={
                'verbose_name': 'Lab Investigation Registry',
                'verbose_name_plural': 'Lab Investigation Registry',
            },
        ),
        migrations.AlterUniqueTogether(
            name='imaginginvestigationregistry',
            unique_together={('modality', 'area_studied')},
        ),
    ]
