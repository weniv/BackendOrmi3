from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# def signup(request):
#     pass

signup = CreateView.as_view(
    form_class = UserCreationForm,
    template_name = 'accounts/form.html',
    success_url = settings.LOGIN_URL,
)

# def login(request):
#     pass

login = LoginView.as_view(
    template_name = 'accounts/form.html',
    # next_page = settings.LOGIN_URL,
)

# def logout(request):
#     pass

logout = LogoutView.as_view(
    next_page = settings.LOGOUT_URL,
)

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


# def logincheck(request):
#     if request.user.is_authenticated:
#         return HttpResponse("로그인 됨!")
#     return HttpResponse("로그인 안됨!")

def logincheck(request):
    print(request.user.is_authenticated)
    print(request.user)
    return render(request, 'accounts/logincheck.html')

def loginfbv(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("login 성공")
        else:
            return HttpResponse("login 실패")
    return render(request, 'accounts/loginfbv.html')