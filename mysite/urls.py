from django.contrib import admin
from django.urls import include, path

from django.contrib.auth import views

# ^ == 문자열이 시작할 때
# & == 문자열이 끝날 때
# \d == 숫자

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('blog.urls')),
]