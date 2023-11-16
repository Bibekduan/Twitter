from django.urls import path
from .import views
from .views import index,SetupProfile,NewPost

urlpatterns = [
    path('index/',index.as_view(),name="index"),
    path('setup_profile/',SetupProfile.as_view(),name="setupprofile"),
    path('new_post/',views.NewPost,name="newpost"),
    path('<username>/follow/<option>/', views.follow_user, name="follow"),
    path('post_detail/<uuid:post_id>/',views.post_detail,name="post_detail"), 
    path('tweet/<uuid:post_id>/',views.tweet,name="tweet"),
    path('like/<uuid:post_id>/',views.like,name="like"),
    path('tweet_detail/<uuid:post_id>/',views.tewwt_detail,name="tweet_detail"),
    path('search/',views.search_user,name="search"),
    path('trend/<slug:tag_slug>/',views.trend,name="trend"),
    path('following/',views.following_user,name="following_post")
]
