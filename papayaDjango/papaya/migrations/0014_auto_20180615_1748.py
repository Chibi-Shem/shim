# Generated by Django 2.0.6 on 2018-06-15 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('papaya', '0013_papayauser_username'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PapayaUser',
            new_name='User',
        ),
    ]
