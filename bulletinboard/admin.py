from django.contrib import admin
from .models import Bulletin, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Bulletin)
class BulletinAdmin(SummernoteModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment', 'bulletin', 'created_on')
    search_fields = ['author', 'comment']
