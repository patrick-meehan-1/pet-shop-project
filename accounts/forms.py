from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.models import Group

class CustomUserCreationForm(UserCreationForm):
    grop = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    class Meta:
        model = CustomUser
        fields = ('username','email','age', 'f_animal')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username','email','age', 'f_animal')
 