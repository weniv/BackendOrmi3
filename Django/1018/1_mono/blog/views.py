from django.shortcuts import render
from .models import Post

def postlist(request):
    posts = Post.objects.all()
    return render(request, 'blog/postlist.html', {'posts':posts})


def postdetail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/postdetail.html', {'post':post})