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
    
        class Meta:
            ordering = ( '-date_added', )

We have a `Post` model to represent our blog's data. Very simple for now, just a post with a title, the content, written by a certain user at a certain time.
The `slug` will be the post url, and is going to be generated from the title.
We're setting the ordering property, so that the recent posts appear first.

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


We'll be adding blog posts through the django admin page, so for starters, lets create a account.

`python manage.py createsuperuser`

Now just go to the `/admin/` url, click on the `add` button on the blog section to add.

If you go back to the home page, now you'll see a list with the titles of the posts you just added.
  
  
Alright, now we need to be able to open individual blog posts.


## blog/urls.py ##

    from django.conf.urls import url
    from . import views
    
    urlpatterns = [
        url( r'^$', views.listAll, name= 'listAll' ),
        url( r'^post/(?P<slug>[-\w]+)$', views.showPost, name= 'showPost' ),
    ]

The url will contain a post slug to identify it.
We're also giving names to the urls, so its easier to reference it in templates, as we'll see below.

## blog/views.py ##

    from django.shortcuts import render, get_object_or_404
    from .models import Post
  
    # (...)
    
    def showPost( request, slug ):
        context = {
            'post': get_object_or_404( Post, slug= slug )
        }
    
        return render( request, 'blog/showPost.html', context )

Nothing too crazy, we try to get a post object and then render the `showPost.html` to display its information. If not found, then we raise a `Http404` exception instead.

## blog/templates/blog/showPost.html ##

    {% extends 'blog/base.html' %}
    
    {% block content %}
        <h1>{{ post.title }} - by {{ post.author }} on {{ post.date_added }}</h1>
        <p>{{ post.content }}</p>
    
        <a href="{% url 'listAll' %}">Back</a>
    {% endblock %}

Here we receive the `post` object we got from the view, and simply show its data.
Notice how we're going back to the blog list page, by using the url names we defined above.

## blog/templates/blog/listAll.html ##

    {% extends 'blog/base.html' %}
    
    {% block content %}
        {% if posts %}
            <ul>
                {% for post in posts %}
                    <li><a href="{% url 'showPost' post.slug %}">{{ post.title }}</a></li>
                {% endfor %}
            </ul>
        {% else %}
            <p>No blog posts yet.</p>
        {% endif %}
    {% endblock %}

There's one more change we need to make, we need to add a link from the blog list to an individual post. Once again, having the named urls makes our lives easier.


# Categories #

Now lets add some categories to the posts.



Now lets add a category list (and have it sorted by the number of posts per category).
Add to the base.html, since we want it always visible


Add a `is_published` property.



Now how to do a blog search.



Voila! We have ourselves a blog. 

