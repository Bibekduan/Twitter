from django import forms
from userauth.models import Profile
from .models import Post


class SetupProfileForm(forms.ModelForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'First name'}),required=True)
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Last name'}),required=True)
    image=forms.ImageField(required=True)
    bio=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Your bio'}),required=True)
    location=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Location'}),required=True)

    class Meta:
        model=Profile
        fields=['first_name','last_name','image','bio','location']


class NewPostForm(forms.ModelForm):
    picture=forms.ImageField(required=False)
    caption=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'What is happening?!'}),required=True)
    tag=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Add tag (comma separated)'}),required=False)

    class Meta:
        model=Post
        fields=['picture','caption','tag']

    
