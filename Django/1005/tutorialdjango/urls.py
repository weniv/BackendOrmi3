from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main.urls')),
    # path('', index),
    # path('about/', about),
    # path('contact/', contact),
    
    path('accounts/', include('accounts.urls')),
    # path('accounts/login', login),
    # path('accounts/logout', logout),

    path('blog/', include('blog.urls')),
    # path('blog/', blog),
    # path('blog/1', blog_1),
    # path('blog/2', blog_2),
    # path('blog/3', blog_3),

    # path('testnotice/<int:pk>', testnotice),
    # path('testlogin/<str:s>', testlogin),
]
