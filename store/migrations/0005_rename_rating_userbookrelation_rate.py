# Generated by Django 4.1.7 on 2023-04-08 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_userbookrelation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbookrelation',
            old_name='rating',
            new_name='rate',
        ),
    ]
