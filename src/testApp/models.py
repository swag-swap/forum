from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import random
import pathlib
from django_ckeditor_5.fields import CKEditor5Field


class Test(models.Model):
    title = models.CharField(max_length=200)
    slug = models.IntegerField(unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="test_author"
    )
    updated_on = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    duration = models.PositiveIntegerField(default=0)
    content = CKEditor5Field('Text', config_name='extends')

    def __str__(self):
        return self.title 
    
    def get_absolute_url(self):
        return reverse("test_detail", kwargs={"slug": str(self.slug)})
    
    def get_manage_url(self):
        return reverse("manage_test", kwargs={"slug": str(self.slug)})
    
    def save(self, *args, **kwargs): 
        if not self.slug:  
            highest_slug = Test.objects.aggregate(models.Max('slug'))
            if highest_slug['slug__max']: 
                new_slug = highest_slug['slug__max'] + 1
            else:
                new_slug = 1   
            self.slug = new_slug
        super().save(*args, **kwargs)


class Question(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    QUESTION_TYPE_CHOICES = (
        ('MCQ', 'Multiple Choice Question'),
        ('MSQ', 'Multiple Select Question'),
        ('THEORY', 'Theory Question'),
    )
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES)
    text = CKEditor5Field('Text', config_name='extends')
    marks = models.IntegerField() 
    
    def __str__(self):
        return self.text
    
    @property
    def display_name(self):
        return self.name or pathlib.Path(self.file.name).name

    def get_download_url(self):
        url_kwargs = { 
            "pk": self.pk,
        }
        return reverse("manage_test", kwargs=url_kwargs)

class Option(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    text = CKEditor5Field('Text', config_name='extends')
    is_correct = models.BooleanField()
 
    def get_download_url(self):
        url_kwargs = { 
            "pk": self.pk,
        }
        return reverse("manage_test", kwargs=url_kwargs)

    def __str__(self):
        return self.text
   

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.test.title}"

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.question.text}"