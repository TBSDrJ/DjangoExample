from django import forms

class PostForm(forms.Form):
    postText = forms.CharField(label = 'Make a New Post',
        widget = forms.Textarea)
