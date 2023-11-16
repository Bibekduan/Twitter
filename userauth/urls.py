from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name="userauth/firstpage.html",redirect_authenticated_user=True),name="firstpage"),
    path('register/',views.Register,name="register"),
    path('login/',views.Login,name="login"),
    path('logout/',views.Logout,name="logout"),
    path('<username>/',views.UserProfile,name="profile"),
]
