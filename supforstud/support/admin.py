from django.contrib import admin

from .models import *

class SupportAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','content', 'time_create','time_update', 'photo', 'is_published',)
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content','id')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create','id')
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Support, SupportAdmin)
admin.site.register(Category, CategoryAdmin)
