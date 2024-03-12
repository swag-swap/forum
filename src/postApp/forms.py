from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget 
from .models import  Comment, Post 
 
input_css_class = "form-control"  


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class


class PostForm(forms.ModelForm):
    # content = RichTextField(config_name='awesome_ckeditor')
    class Meta:
        model = Post
        fields = ['title', 'content','attachment']
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="comment"
            )
        } 
     

class SearchForm(forms.Form):
    query = forms.CharField(label='Search')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class