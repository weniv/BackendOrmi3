from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def notice(request):
    return render(request, 'notice/notice.html')