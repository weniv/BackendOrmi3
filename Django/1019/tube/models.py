from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumb_image = models.ImageField(
        upload_to='tube/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(
        upload_to='tube/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/tube/{self.pk}/'
    
class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.message
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name