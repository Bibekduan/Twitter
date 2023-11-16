from django.contrib import admin
from . models import Post,Tag,Follow,Stream,Likes
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=['user','picture','posted','like']



class FollowAdmin(admin.ModelAdmin):
    list_display=['follower','following']

class StreamAdmin(admin.ModelAdmin):
    list_display=['user','post']

class LikesAdmin(admin.ModelAdmin):
    list_display=['user','post']


admin.site.register(Post,PostAdmin)
admin.site.register(Tag)
admin.site.register(Follow,FollowAdmin)
admin.site.register(Stream,StreamAdmin)
admin.site.register(Likes,LikesAdmin)