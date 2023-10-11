from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 처음 생성될 때만
    updated_at = models.DateTimeField(auto_now=True) # 수정될 때마다

    def __str__(self):
        time = self.created_at.strftime('%Y-%m-%d %H:%M')
        return f'제목: {self.title}, 시간: {time}'
