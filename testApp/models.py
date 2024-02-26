from django.db import models
from app.models import CustomUser
from django.urls import reverse
from django.utils.text import slugify
import random


class Test(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="test_author"
    )
    updated_on = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    content = models.TextField()
    questions = models.ManyToManyField('Question')

    def __str__(self):
        return self.title 
    
    def get_absolute_url(self):
        return reverse("test_detail", kwargs={"slug": str(self.slug)})
    

    def create_unique_slug(self, new_slug=None):
        if new_slug is not None:
            slug = new_slug
        else:
            slug = slugify(self.title)

        queryset = Test.objects.filter(slug=slug).exclude(id=self.id)
        if queryset.exists():
            random_number = random.randint(1, 1000)
            new_slug = f"{slug}-{random_number}"
            return self.create_unique_slug(new_slug=new_slug)
        return slug
 


class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('MCQ', 'Multiple Choice Question'),
        ('MSQ', 'Multiple Select Question'),
        ('THEORY', 'Theory Question'),
    )
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES)
    text = models.TextField()
    images = models.ManyToManyField('QuestionImage', blank=True)
    marks = models.IntegerField()
    options = models.ManyToManyField('Option')

    def __str__(self):
        return self.text

class Option(models.Model):
    text = models.CharField(max_length=200)
    images = models.ManyToManyField('OptionImage', blank=True)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.text

class QuestionImage(models.Model): 
    image = models.ImageField(upload_to='question_images/')

    def __str__(self):
        return self.image.name

class OptionImage(models.Model): 
    image = models.ImageField(upload_to='option_images/')

    def __str__(self):
        return self.image.name

class TestResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.test.title}"

class Response(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.question.text}"
