from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import auth
from .models import Profile
from django.db.models import Q
from post.models import Follow,Post,Tag
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# Create your views here.
def FirstPage(requset):
    return render(requset,"userauth/firstpage.html")
    

def Register(request):
    if request.method == 'POST':    
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email Is Already Used")
                return redirect('register')
            elif User.objects.filter(username=username):
                messages.info(request,"Username Is Already Used")
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request,"Password Are Not Match")
            return redirect('register')
    else:
        return render(request,"userauth/register.html")


def Login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=auth.authenticate( request,username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,"Invalid login credentials. Please try again.")
            return redirect('login')
    else:
        return render(request,"userauth/login.html")
    


def Logout(request):
    auth.logout(request)
    return redirect('index')



#profile view:
@login_required
def UserProfile(request,username):
    user=get_object_or_404(User,username=username)
    profile, created=Profile.objects.get_or_create(user=user)

    #trends on twitter
    trends=Tag.objects.all()[:5]

    #search function
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

    following_status = False  # Default to not following
    following_count = 0
    followers_count = 0

    #treaking status
    if request.user.is_authenticated:
        following_status=Follow.objects.filter(following=user,follower=request.user).exists()
        following_count=Follow.objects.filter(follower=user).count()
        followers_count=Follow.objects.filter(following=user).count()

    posts=Post.objects.filter(user=user).order_by('-posted')[:5]

    context={
        'profile':profile,
        'following_status':following_status,
        'following_count':following_count,
        'followers_count':followers_count,
        'posts':posts,
        'user':user,
        'trends':trends,
        'users':users,
        'query':query
    }
    return render(request,"userauth/profile.html",context)



    