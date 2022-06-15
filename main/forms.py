from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import User

class Register_Form(UserCreationForm):
    email=forms.EmailField(required=True, help_text='required')
    first_name=forms.CharField(max_length=32,required=False, help_text='optional')
    last_name=forms.CharField(max_length=32,required=False, help_text='optional')
    
    class Meta:
        model= User
        fields= ['username', 'avatar', 'first_name', 'last_name', 'email', 'password1', 'password2']

class User_update_Form(UserCreationForm):
    email=forms.EmailField(required=True, help_text='required')
    # first_name=forms.CharField(max_length=32,required=False, help_text='optional')
    # last_name=forms.CharField(max_length=32,required=False, help_text='optional')
    
    class Meta:
        model= User
        fields= [ 'email']

class Reader_Register_Form(Register_Form):

    def save(self, *args, **kwargs):
        user=super().save(commit=False)
        user.is_reader=True
        user.save()
        return user

class Poster_Register_Form(Register_Form):

    def save(self, *args, **kwargs):
        user=super().save(commit=False)
        user.is_poster=True
        user.save()
        return user
