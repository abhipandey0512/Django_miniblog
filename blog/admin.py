from django.contrib import admin
from .models import  blog_post

# Register your models here.
@admin.register(blog_post)
class PostModeAdmin(admin.ModelAdmin):
    list_dispaly =['id','title','desc']
