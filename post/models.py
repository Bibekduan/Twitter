from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse
from django.utils.text import slugify


import uuid
from django.db.models.signals import post_delete,post_save

# Create your models here.


# Uploading user files to a specific directory
def user_directory_path(instance, filename) :
    return 'user_{0}/{1}' .format(instance.user.id,filename)

#craete tag mogel
class Tag(models.Model):
    title=models.CharField( max_length=100,verbose_name="tag")
    slug=models.SlugField(null=False,unique=True,default=uuid.uuid1)

    class Meta:
        verbose_name= 'Tag'
        verbose_name_plural= 'Tags'

    def get_absolute_url(self):
        return reverse("tags", args=[self.slug])
    
    def __str__(self):
        return self.title
    
    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug - slugify(self.slug)
        return super().save(*args,**kwargs)



#display all post for user
class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    picture=models.ImageField(upload_to=user_directory_path,null=True,verbose_name="Picture",blank=True)
    caption=models.CharField(max_length=1000,verbose_name="Caption")
    posted=models.DateTimeField(auto_now_add=True)
    tag=models.ManyToManyField(Tag,related_name="Tags")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
   


    def __str__(self):
        return self.caption




# create follow models:
class Follow(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")


#create a stream page where all post will be display only the following user
class Stream(models.Model):
    following=models.ForeignKey(User, related_name="stream_following", on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="stream_user")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    date=models.DateField()

    def add_post(sender,instance,*args, **kwargs):
        post=instance
        user=post.user
        followers=Follow.objects.filter(following=user)
        for follower in followers:
            stream=Stream(post=post,user=follower.follower,date=post.posted,following=user)
            stream.save()


#create a models that user can like the post:
class Likes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_likes")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_like")


post_save.connect(Stream.add_post,sender=Post)