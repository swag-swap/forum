from django import forms
from ckeditor.fields import RichTextField
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Comment, Post

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(required=False)
    profile_picture = forms.ImageField(required=False) 
    
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('date_of_birth', 'profile_picture')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]


class PostForm(forms.ModelForm):
    content = RichTextField(config_name='awesome_ckeditor')
    class Meta:
        model = Post
        fields = ['title', 'content','attachment']

class SearchForm(forms.Form):
    query = forms.CharField(label='Search')