# Generated by Django 2.2.7 on 2019-11-26 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0006_auto_20191125_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='picture',
            field=models.ImageField(upload_to='fs'),
        ),
    ]
