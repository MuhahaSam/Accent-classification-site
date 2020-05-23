from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['record', 'data_id']
        widgets = {
            'record':forms.FileInput(attrs={'class':"form-control-file"})
        }




class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email' ,'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'type':'email'}),
            'password1':forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
            'password2':forms.TextInput(attrs={'class': 'form-control', 'type': 'password'})
        }














