# Generated by Django 2.2.7 on 2019-11-24 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0004_auto_20191124_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('mobile_1', models.CharField(max_length=13)),
                ('mobile_2', models.CharField(max_length=13)),
                ('work_address', models.CharField(max_length=200)),
                ('work_mobile', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]