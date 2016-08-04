from django.contrib import admin
from blog.models import Post, Category


class CategoryAdmin( admin.ModelAdmin ):
    list_display = [ 'name', ]
    prepopulated_fields = { 'slug': ( 'name', ) }


class PostAdmin( admin.ModelAdmin ):
    list_display = [ 'title', 'author', 'date_added' ]
    list_filter = [ 'date_added', 'categories' ]
    search_fields = [ 'title', 'content' ]
    date_hierarchy = 'date_added'
    prepopulated_fields = { 'slug': ( 'title', ) }
    filter_horizontal = ( 'categories', )

admin.site.register( Post, PostAdmin )
admin.site.register( Category, CategoryAdmin )
