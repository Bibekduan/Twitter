from django.db import models
from django.contrib.auth.models import User
from post.models import Post
# Create your models here.
class Tweet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="tweets")
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    