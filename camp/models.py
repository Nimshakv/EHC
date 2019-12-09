from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.files.storage import FileSystemStorage
from camp_reg import settings

fs = FileSystemStorage(location=settings.MEDIA_ROOT)



class User(AbstractUser):
    is_parent = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


class Parent(models.Model):
    address = models.CharField(max_length=200)
    mobile_1 = models.CharField(max_length=13)
    mobile_2 = models.CharField(max_length=13, blank=True)
    work_address = models.CharField(max_length=200, blank=True)
    work_mobile = models.CharField(max_length=13, blank=True)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Student(models.Model):
    # SAMALIYAH_SUMMER = 'SR'
    # SAMALIYAH_SPRING = 'SG'
    # ATHURAYA = 'AT'
    # RAMADAN_FESTIVAL = 'RF'
    #
    # CAMP_CHOICES = [
    #     ('samaliyah_summer', SAMALIYAH_SUMMER),
    #     ('samaliyah_spring', SAMALIYAH_SPRING),
    #     ('athuraya', ATHURAYA),
    #     ('ramadan_festival', RAMADAN_FESTIVAL)
    # ]

    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, default='male')
    school = models.CharField(max_length=200)
    grade = models.CharField(max_length=10)
    dob = models.DateField()
    contact = models.CharField(max_length=13)
    email = models.EmailField()
    camp = models.CharField(max_length=100)
    picture = models.ImageField(storage=fs)
    id_card = models.FileField(storage=fs, default=None)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)