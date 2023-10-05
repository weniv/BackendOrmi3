from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

db = {
    1: {
        'title': '제목 1', 
        'contents': 'Post 1 body', 
        'img': 'https://picsum.photos/200/300'
        },
    2: {
        'title': '제목 2', 
        'contents': 'Post 2 body', 
        'img': 'https://picsum.photos/200/300'
        },
    3: {
        'title': '제목 3', 
        'contents': 'Post 3 body', 
        'img': 'https://picsum.photos/200/300'
        },
    'i': {
        'hello'
    }
}

def blog(request):
    # db = Cafe.objects.all()
    return render(request, 'blog/blog.html', {'db': db})

def post(request, pk):
    # db = Cafe.objects.get(pk=pk)
    if db.get(pk):
        return render(request, 'blog/post.html', {'post': db.get(pk)})
    else:
        return HttpResponse('잘못된 접근입니다!')


def bookinfo(request):
    '''
    교육용 크롤링 페이지입니다.
    '''
    url = 'https://paullab.co.kr/bookservice/'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    result = [f'<p>{i.text}</p>' for i in soup.select('.book_name')]
    return HttpResponse(result)