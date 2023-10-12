from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView

# def signup(request):
#     pass

signup = CreateView.as_view(
    form_class = UserCreationForm,
    #기본 URL을 변경
    template_name = 'accounts/form.html',
    #로그인 성공했을 때 보낼 URL
    success_url = settings.LOGIN_URL,
)

# def login(request):
#     pass

login = LoginView.as_view(
    template_name = 'accounts/form.html',
)

# def logout(request):
#     pass

logout = LogoutView.as_view(
    next_page = settings.LOGIN_URL,
)

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')