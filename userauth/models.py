from django.db import models
from django.contrib.auth.models import User
from post.models import Tag
from django.db.models.signals import post_save
# Create your models here.

def user_directory_path(instance, filename) :
    return 'user_{0}/{1}' .format(instance.user.id,filename)



class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    first_name=models.CharField(max_length=40 ,null=True,blank=True)
    last_name=models.CharField(max_length=40,null=True,blank=True)
    location=models.CharField(max_length=200,null=True,blank=True)
    url=models.URLField(max_length=1000,null=True,blank=True)
    bio=models.TextField(max_length=150,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to=user_directory_path,null=True,blank=True,verbose_name="Picture",default="default.jpg")
   



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile,sender=User)
