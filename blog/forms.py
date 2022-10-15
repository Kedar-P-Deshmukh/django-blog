from cProfile import label
from django import forms
from .models import Comment

class CommentsForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        exclude = ["post"]
        label={
            "user_name":"Your Name",
            "user_emial":"Your Email",
            "text": "comments"
        }