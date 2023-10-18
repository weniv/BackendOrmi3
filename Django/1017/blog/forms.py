from django import forms
from .models import Post

class CommentForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

class PostForm(forms.ModelForm):
    # 예시입니다.
    class Meta:
        model = Post
        fields = '__all__'