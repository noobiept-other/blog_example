from django.contrib import admin
from blog.models import Post


class PostAdmin( admin.ModelAdmin ):

    list_display = [ 'title', 'author', 'date_added' ]
    list_filter = [ 'date_added' ]
    search_fields = [ 'title', 'content' ]
    date_hierarchy = 'date_added'
    prepopulated_fields = { 'slug': ( 'title', ) }

admin.site.register( Post, PostAdmin )
