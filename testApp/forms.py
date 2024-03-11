from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Test, Question

input_css_class = "form-control"


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'start_time', 'duration','content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class


class TestUpdateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["title", 'start_time', 'duration', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_type", 'text', 'marks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            if field in ['is_free', 'active']:
                continue
            self.fields[field].widget.attrs['class'] = input_css_class


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
