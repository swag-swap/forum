from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Test, Question, Option
from django_ckeditor_5.widgets import CKEditor5Widget

input_css_class = "form-control" 


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'start_time', 'end_time','content']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        # widgets = {
        #     "content": CKEditor5Widget(
        #         attrs={"class": "django_ckeditor_5"}, config_name="extends"
        #     )
        # } 
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.fields["content"].required = False 
        # self.fields["content"].widget.attrs['id'] = "summernote"

        # for field in self.fields:
        #     if field in ['content']:
        #         continue
        #     self.fields[field].widget.attrs['class'] = input_css_class


class TestUpdateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["title", 'start_time', 'end_time', 'content'] 
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        } 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False
        self.fields['start_time'].widget.attrs['type'] = 'datetime-local'
        self.fields['end_time'].widget.attrs['type'] = 'datetime-local'
        # for field in self.fields:
        #     if field in ['content']:
        #         continue
        #     self.fields[field].widget.attrs['class'] = input_css_class



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_type", 'text', 'marks']
        # widgets = {
        #     "text": CKEditor5Widget(
        #         attrs={"class": "django_ckeditor_5"}, config_name="extends"
        #     )
        # } 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].required = False
        # for field in self.fields:
        #     if field in ['is_free', 'active','text']:
        #         continue
        #     self.fields[field].widget.attrs['class'] = input_css_class


TestQuestionModelFormSet = modelformset_factory(
    Question,
    form=QuestionForm,
    fields = ['question_type', 'text','marks'],
    extra=0,
    can_delete=True
)

TestQuestionInlineFormSet = inlineformset_factory(
    Test,
    Question,
    form = QuestionForm,
    formset = TestQuestionModelFormSet,
    fields = ['question_type', 'text','marks'],
    extra=0,
    can_delete=True
)

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["text", "is_correct"]
        # widgets = {
        #     "text": CKEditor5Widget(
        #         attrs={"class": "django_ckeditor_5"}, config_name="extends"
        #     )
        # } 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].required = False

QuestionOptionModelFormSet = modelformset_factory(
    Option,
    form=OptionForm,
    fields = ["text", "is_correct"],
    extra=0,
    can_delete=True
)

QuestionOptionInlineFormSet = inlineformset_factory(
    Question,
    Option,
    form = OptionForm,
    formset = QuestionOptionModelFormSet,
    fields = ["text", "is_correct"],
    extra=0,
    can_delete=True
)

OptionFormSet = inlineformset_factory(
    Question,
    Option,
    form=OptionForm,
    fields=['text', 'is_correct'],
    extra=1,  # Number of extra empty forms
    can_delete=True
)