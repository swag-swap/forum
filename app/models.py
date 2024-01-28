from django.db import models  
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from ckeditor.fields import RichTextField

class CustomUser(AbstractUser): 
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
 
    
    def __str__(self):
        return self.username
    
    
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="post_author"
    )
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)  

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": str(self.slug)})
 


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 

    class Meta:
        ordering = ["created_on"]

    def __str__(self): 
        return "Comment {} by {}".format(self.body, self.author.username)

