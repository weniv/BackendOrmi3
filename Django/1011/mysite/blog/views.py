from django.shortcuts import render, redirect
from .models import Post

def blog(request):
    db = Post.objects.all()
    context = {
        'db': db,
    }
    return render(request, 'blog/blog.html', context)

def post(request, pk):
    db = Post.objects.get(pk=pk)
    context = {
        'db': db,
    }
    return render(request, 'blog/post.html', context)

def test(request):
    return render(request, 'blog/test.txt')

def posttest(request, pk):
    q = Post.objects.create(title=f'{pk}', contents=f'{pk}{pk}')
    q.save()
    return redirect('blog')

def postdel(request, pk):
    q = Post.objects.get(pk=pk)
    q.delete()
    return redirect('blog')