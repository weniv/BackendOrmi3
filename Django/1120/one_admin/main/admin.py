from django.contrib import admin
from .models import Post
from django.utils.safestring import mark_safe

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo_tag', 'title', 'content', 'created_at', 'updated_at']
    list_display_links = ['title']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title']
    list_per_page = 10

    def photo_tag(self, post):
        if post.photo:
            return mark_safe(f'<img src="{post.photo.url}" style="width: 100px;" />')
        return None