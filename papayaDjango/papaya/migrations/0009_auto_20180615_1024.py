# Generated by Django 2.0.6 on 2018-06-15 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papaya', '0008_auto_20180615_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(default='papaya/media/papaya/empty.png', upload_to='papaya/media/papaya'),
        ),
    ]
