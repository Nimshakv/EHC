from .models import User
from .models import Student, Parent
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_parent', 'is_staff')


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'