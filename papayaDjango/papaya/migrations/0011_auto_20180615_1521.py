# Generated by Django 2.0.6 on 2018-06-15 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papaya', '0010_auto_20180615_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='papayauser',
            name='email',
            field=models.EmailField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='papayauser',
            name='fname',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='papayauser',
            name='lname',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='papayauser',
            name='username',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='papayauser',
            name='image',
            field=models.ImageField(default='papaya/static/papaya/images/anon.jpeg', upload_to='papaya/static/papaya/images'),
        ),
    ]
