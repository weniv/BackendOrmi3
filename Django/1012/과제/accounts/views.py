from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

signup = CreateView.as_view(
    form_class = UserCreationForm,
    template_name = 'accounts/form.html',
)


login = LoginView.as_view(
    template_name = 'accounts/form.html',
)

logout = LogoutView.as_view()

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')