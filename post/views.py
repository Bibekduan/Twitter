from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth.models import User
from .models import Post,Follow,Stream,Likes,Tag
from django.db.models import Q
from django.contrib import messages
from userauth.models import Profile
from tweet.models import Tweet
from tweet.forms import TweetPostForm
from django.db import transaction
from .forms import SetupProfileForm,NewPostForm


# Create your views here.
method_decorator(login_required,name="dispatch")
class index(View):
    def get(self, request, *args, **kwargs):
        user=request.user
        all_user=User.objects.all()[:3]

        all_posts=Post.objects.all().order_by('-posted')
        
        #get search result
        query=request.GET.get('q')
        if query is not None:   
            users=User.objects.filter(
                Q(username__icontains = query) |
                Q(profile__first_name__icontains = query) |
                Q(profile__last_name__icontains = query) |
                Q(profile__bio__icontains = query)

            ).distinct()
        else:
            users=[]

        # trend for user
        trends=Tag.objects.all()[:5]


        context={
            # 'post_item':posts,
            'user':user,
            'all_posts':all_posts,
            'all_user':all_user,
            'users':users,
            'query':query,
            'trends':trends
            
        }
        return render(request,'index.html',context)

method_decorator(login_required,name="dispatch")
class SetupProfile(View):
    def post(self,request,*args, **kwargs):  
        user_profile=Profile.objects.get(user=request.user)
        if request.method == 'POST':
            form=SetupProfileForm(request.POST,request.FILES,instance=user_profile)
            if form.is_valid():
                form.save()
                messages.success(request,"Profile updated successfully!")
                return redirect('profile',username=user_profile.user.username)
            else:
                messages.error(request,"Error updating profile. Please check the form.")
        else:
            form=SetupProfileForm(instance=user_profile)

        context={
            'form':form,
        }
        return render(request,"userauth/setup_profile.html",context)
    

@login_required
def NewPost(request):
    if request.method == 'POST':
        form=NewPostForm(request.POST,request.FILES)
        if form.is_valid():
            picture=form.cleaned_data['picture']
            caption=form.cleaned_data['caption']
            tags=form.cleaned_data['tag'].split(',') # Split tags by commas

            # Create a new post
            post=Post(picture=picture,caption=caption,user=request.user)
            post.save()

             # Add tags to the post
            for tag in tags:
                post.tag.create(title=tag.strip())  # Strip whitespace from tags
            return redirect('index')
        else:
                messages.error(request, "Error updating post. Please check the form.")
         
    else:
        form=NewPostForm()
            
    context={
        'form':form
    }
    return render(request,"newpost.html",context)

@login_required
def follow_user(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try:
        f, created = Follow.objects.get_or_create(follower=user, following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=user).all().delete()
        else:
            posts = Post.objects.filter(user=following)[:10]

            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user, date=post.posted, following=following)
                    stream.save()

        return HttpResponseRedirect(reverse('profile', args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))


@login_required
def post_detail(request,post_id):
    post=get_object_or_404(Post,id=post_id)

    #Tweet
    tweet=Tweet.objects.filter(post=post).order_by('-date')

    #Tweet form
    if request.method == 'POST':
        form=TweetPostForm(request.POST,request.FILES)
        if form.is_valid():
            new_tweet=form.save(commit=False)
            new_tweet.post=post
            new_tweet.user=request.user
            new_tweet.save()
            return redirect('post_detail',post_id=post_id)
    else:
        form=TweetPostForm()


    context={
         'post':post,
         'form':form,
         'tweet':tweet
    }
    return render(request,"post_detail.html",context)


@login_required
def tweet(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    user=request.user
    reply=Tweet.objects.filter(user=user,post=post).count()

    #tweet form
    if request.method == 'POST':
        form=TweetPostForm(request.POST,request.FILES)
        if form.is_valid:
            tweet_form=form.save(commit=False)
            tweet_form.post=post
            tweet_form.user=request.user
            tweet_form.save()
            return redirect('index')
        
    else:
        form=TweetPostForm()
    context={
        'post':post,
        'form':form,
        'reply':reply
    }
    return render(request,"tweet.html",context)



@login_required
def like(request,post_id):
    user=request.user
    post=get_object_or_404(Post,id=post_id)

    current_like=post.like
    liked=Likes.objects.filter(user=user,post=post).count()

    if not liked:
        liked=Likes.objects.create(user=user,post=post)
        current_like=current_like + 1
    else:
        liked=Likes.objects.filter(user=user,post=post).delete()
        current_like=current_like - 1

    post.like=current_like
    post.save()
    return redirect('index')



@login_required
def tewwt_detail(request,post_id):
   
    post=get_object_or_404(Post,id=post_id)
    all_tweet=Tweet.objects.filter(post=post).order_by('-date')

    #trends on twitter
    trends=Tag.objects.all()[:5]

    #user list
    all_user=User.objects.all()[:3]


    if request.method == "POST":
        form=TweetPostForm(request.POST,request.FILES)
        if form.is_valid():
            tewwt_details=form.save(commit=False)
            tewwt_details.post=post
            tewwt_details.user=request.user
            tewwt_details.save()
            return redirect('tweet_detail',post_id=post_id)
    else:
        form=TweetPostForm()

    context={
        'form':form,
        'post':post,
        'all_tweet':all_tweet,
        'trends':trends,
        'all_user':all_user
    }
    return render(request,"tweet_detail.html",context)



@login_required
def search_user(request):
    all_user=User.objects.all()

    query=request.GET.get('q')
    if query is not None:         
        users=User.objects.filter(
            Q(username__icontains=query) |
            Q(profile__bio__icontains=query) | 
            Q(profile__first_name__icontains=query) |
            Q(profile__last_name__icontains=query)
        ).distinct()
    else:
        users=[]   

    #trend for user
    trends=Tag.objects.all()[0:5]
      
    context={
        'users':users,
        'query':query,
        'trends':trends,
        'all_user':all_user
    }
    return render(request,"search.html",context)


@login_required
def trend(request,tag_slug):
    tag=get_object_or_404(Tag,slug=tag_slug)
    posts=Post.objects.filter(tag=tag).order_by('-posted')
    all_user=User.objects.all()


    tag_count=posts.count()
    
    # profile_list=[]
    # for post in posts:
    #     user_profile=Profile.objects.filter(user=post.user,tag=tag).first()
    #     if user_profile:
    #         profile_list.append(user_profile)

    # profile_set=set(profile_list)
    # profiles=list(profile_set)[:2]
    trends=Tag.objects.all()[:5]

    #search function
    query=request.GET.get('q')
    if query is not None:   
        users=User.objects.filter(
            Q(username__icontains = query) |
            Q(profile__first_name__icontains = query) |
            Q(profile__last_name__icontains = query) |
            Q(profile__bio__icontains = query)

        ).distinct()
    else:
        users=[]
    context={
        'posts':posts,
        # 'profiles':profiles,
        'trends':trends,
        'tag':tag,
        'query':query,
        'users':users,
        'tag_count':tag_count,
        'all_user':all_user
    }
    return render(request,"trend.html",context)


#display following user
@login_required
def following_user(request):
    user=request.user
    all_user=User.objects.all()
    #display following user post display
    following_users=Follow.objects.filter(follower=user).values_list('following',flat=True)
    posts=Post.objects.filter(Q(user=user) | Q(user__in=following_users)).order_by('-posted')

    #search function
    query=request.GET.get('q')
    if query is not None:   
        users=User.objects.filter(
            Q(username__icontains = query) |
            Q(profile__first_name__icontains = query) |
            Q(profile__last_name__icontains = query) |
            Q(profile__bio__icontains = query)

        ).distinct()
    else:
        users=[]

    # trend for user
    trends=Tag.objects.all()[:5]
    context={
        'posts':posts,
        'trends':trends,
        'users':users,
        'query':query,
        'all_user':all_user
    }
    return render(request,"following.html",context)