from django import forms
from .models import Tweet



class TweetPostForm(forms.ModelForm):
    body=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Post your reply'}))

    class Meta:
        model=Tweet
        fields=['body']