from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Comments

class Register_Form(UserCreationForm):
    email=forms.EmailField(required=True, help_text='required and unique')
    first_name=forms.CharField(max_length=32,required=False, help_text='optional')
    last_name=forms.CharField(max_length=32,required=False, help_text='optional')
    
    class Meta:
        model= User
        fields= ['username', 'avatar', 'first_name', 'last_name', 'email', 'password1', 'password2']

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


class Comments_Form(forms.ModelForm):
    # name=forms.ForeignField(max_length=32, help_text='(your name here)', required=False)
    class Meta:
        model= Comments
        fields= ['text']
    
    
    def delete(self, *args, **kwargs):
        comment = Comments.objects.filter(id=self.pk)
        comment.delete()
        print('deleted!')

    # def save(self, *args, **kwargs):
    #     comment=super().save(commit=False)
    #     if comment.name.is_authenticated:
    #         comment.save()
    #     else:
    #         comment.name=null
    #         comment.save()        
    #     return comment
   
