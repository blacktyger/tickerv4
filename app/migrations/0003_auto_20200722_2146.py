# Generated by Django 3.0.8 on 2020-07-22 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='ath',
        ),
        migrations.RemoveField(
            model_name='history',
            name='ath_change',
        ),
        migrations.RemoveField(
            model_name='history',
            name='ath_date',
        ),
        migrations.RemoveField(
            model_name='history',
            name='last_block',
        ),
        migrations.RemoveField(
            model_name='history',
            name='percentage_change_24h',
        ),
        migrations.RemoveField(
            model_name='history',
            name='percentage_change_7d',
        ),
        migrations.RemoveField(
            model_name='history',
            name='to_save',
        ),
    ]
