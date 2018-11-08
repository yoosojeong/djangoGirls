from django.contrib import admin
from .models import Post, Comment

# Post모델을 등록하겠다.
admin.site.register(Post)
admin.site.register(Comment)
