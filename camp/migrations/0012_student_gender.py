# Generated by Django 2.2.7 on 2019-11-26 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0011_auto_20191126_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(default='male', max_length=10),
        ),
    ]