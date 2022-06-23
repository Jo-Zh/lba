from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Posts, Category, Comments,Notes

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
    prepopulated_fields = {"slug": ("name",)} 

class CommentsAdmin(admin.ModelAdmin):
    list_display=("id","post","parent","date")

class PostsAdmin(admin.ModelAdmin):
    list_display=("title", "date", "id", "cover")
    ordering=("-date",)

admin.site.register(User, UserAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Notes)

