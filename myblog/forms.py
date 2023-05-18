from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class AddPostForm(forms.ModelForm):
    class Meta:
        model=Post
        exclude= ('user','date',)
        fields=('author','title','description','post_image','date')

        widgets = {
            'author':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Author Name'}),
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Title'}),
            'description':forms.Textarea(attrs={'class':'form-control'})

        }

class AddCommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        exclude= ('post','added_date')
        fields=('name','body','added_date')

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Name'}),
            'body':forms.Textarea(attrs={'class':'form-control'})

        }