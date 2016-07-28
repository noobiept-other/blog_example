Lets do a simple blog with django.

Initialize the project.

`django-admin startproject blog_example`


We'll assume this blog is part of a bigger website, so we'll try to contain all our files in a single place.

We'll create a django application to keep it separated from the rest, and to be easy to add to any other website.

`python manage.py startapp blog`

Then add to the settings.

    INSTALLED_APPS = [
        # ...
        'blog',
    ]

And add the urls.

## blog_example/urls.py ##

    from django.conf.urls import url, include
    from django.contrib import admin
    
    urlpatterns = [
        url( r'^', include( 'blog.urls' ) ),
        url( r'^admin/', admin.site.urls ),
    ]

The url pattern can be different, I'll be matching the blog urls since the root, but you could change it to `r'^blog/'` for example. Make sure the pattern is open-ended (without the `$`) so it can continue to try to match with the rest of the blog urls.

Now lets work on our `blog` django application.

First start with the model.

## blog/models.py ##

    from django.db import models
    from django.contrib.auth.models import User
    from django.utils import timezone
    
    class Post( models.Model ):
    
        author = models.ForeignKey( User )
        title = models.CharField( max_length= 100 )
        slug = models.SlugField( max_length= 100, unique= True )
        content = models.TextField()
        date_added = models.DateTimeField( default= timezone.now )

We have a `Post` model to represent our blog's data. Very simple for now, just a post with a title, the content, written by a certain user at a certain time.
The `slug` will be the post url, and is going to be generated from the title.

We'll take advantage of the django admin page, to add the blog posts, so we'll need to set some things before that is possible.

## blog/admin.py ##

    from django.contrib import admin
    from blog.models import Post
        
    class PostAdmin( admin.ModelAdmin ):
    
        list_display = [ 'title', 'author', 'date_added' ]
        list_filter = [ 'date_added' ]
        search_fields = [ 'title', 'content' ]
        date_hierarchy = 'date_added'
        prepopulated_fields = { 'slug': ( 'title', ) }
    
    admin.site.register( Post, PostAdmin )

Some basic admin configuration. Note that we're setting the `slug` field to be automatically populated based on the title.

Now that we have our data defined, time to display it! For now we'll simply show a list of all the added posts.


## blog/urls.py ##

    from django.conf.urls import url
    from . import views
    
    urlpatterns = [
        url( r'^$', views.listAll ),
    ]

## blog/views.py ##

    from django.shortcuts import render
    from .models import Post
    
    def listAll( request ):
        context = {
            'posts': Post.objects.all()
        }
    
        return render( request, 'blog/listAll.html', context )

## blog/templates/blog/base.html ##

    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8" />
            <title>Blog</title>        
        </head>
    <body>
        <div>{% block content %}{% endblock %}</div>
    </body>
    </html>

## blog/templates/blog/listAll.html ##

    {% extends 'blog/base.html' %}
    
    {% block content %}
        {% if posts %}
            <ul>
                {% for post in posts %}
                    <li>{{ post.title }}</li>
                {% endfor %}
            </ul>
        {% else %}
            <p>No blog posts yet.</p>
        {% endif %}
    {% endblock %}

By default, any files in a `templates` directory on each application will be added to the search path of templates by django. We're adding an extra `blog` folder to avoid name collisions with other applications. When we want to reference the `listAll.html` for example, we use the `blog/listAll.html`, so its obvious where this template belongs to.

Now time to apply all migrations to the database.

`python manage.py makemigrations`
`python manage.py migrate`

And start the server.

`python manage.py runserver`


Show how to add a blog post with the django admin.

  
Alright, now we need to be able to open individual blog posts.
 
urls / views / templates

Now lets add a category list (and have it sorted by the number of posts per category).


Add a `is_published` property.



Now how to do a blog search.



Voila! We have ourselves a blog. 

