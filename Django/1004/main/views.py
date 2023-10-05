from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    return render(request, 'logout.html')

def blog(request):
    return render(request, 'blog.html')

def blog_1(request):
    return render(request, 'blog_1.html')

def blog_2(request):
    return render(request, 'blog_2.html')

def blog_3(request):
    return render(request, 'blog_3.html')

def testnotice(request, pk):
    print(pk)
    # DB에서 pk에 해당하는 데이터를 가져옵니다.
    return render(request, 'testnotice.html', {'pk': pk})

def testlogin(request, s):
    print(s)
    if s == 'login':
        return render(request, 'testlogin.html', {'s': s + ', 로그인 페이지'})
    elif s == 'logout':
        return render(request, 'testlogin.html', {'s': s + ', 로그아웃 페이지'})
    else:
        return render(request, 'testlogin.html', {'s': 'error'})