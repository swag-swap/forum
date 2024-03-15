from django.utils.text import slugify
from django.db import models  
from django.contrib.auth.models import User
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
import random

# class CustomUser(AbstractUser): 
#     date_of_birth = models.DateField(null=True, blank=True)
#     profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
  

#     def __str__(self):
#         return self.username
    
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_author"
    )
    updated_on = models.DateTimeField(auto_now=True)
    text = CKEditor5Field('Text', config_name='extends')
    attachment = models.FileField(upload_to='post_attachments/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)  

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": str(self.slug)})
    

    def create_unique_slug(self, new_slug=None):
        if new_slug is not None:
            slug = new_slug
        else:
            slug = slugify(self.title)

        queryset = Post.objects.filter(slug=slug).exclude(id=self.id)
        if queryset.exists():
            random_number = random.randint(1, 1000)
            new_slug = f"{slug}-{random_number}"
            return self.create_unique_slug(new_slug=new_slug)
        return slug
 


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 

    class Meta:
        ordering = ["created_on"]

    def __str__(self): 
        return "Comment {} by {}".format(self.body, self.author.username)
