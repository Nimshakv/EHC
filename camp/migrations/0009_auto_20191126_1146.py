# Generated by Django 2.2.7 on 2019-11-26 11:46

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0008_auto_20191126_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='picture',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='/media'), upload_to=''),
        ),
    ]
