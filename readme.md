Lets do a simple blog with django.

We'll write it step by step, starting first by showing a list of posts, then how to open an individual post. We'll add some categories and then finally add some simple search functionality.

The code is available in this project as well (click on the `source` tab).

# First Steps #

Lets start by initializing the project.

`django-admin startproject blog_example`

We'll assume this blog is part of a bigger website, so we'll try to contain all our files in a single place. We do that by creating a django application to hold our code.

`python manage.py startapp blog`

Then we need to register it in the project settings, and set up the application urls as well.

## blog_example/settings.py ##

    INSTALLED_APPS = [
        # ...
        'blog',
    ]

## blog_example/urls.py ##

    from django.conf.urls import url, include
    from django.contrib import admin
    
    urlpatterns = [
        url( r'^', include( 'blog.urls' ) ),
        url( r'^admin/', admin.site.urls ),
    ]

I'm matching the blog urls from the root, but you could change it to anything else, for example `r'^blog/'`. Make sure the pattern is open-ended (without the `$`) so it can continue to try to match with the rest of the blog urls.

## Posts List ##

For now, we focus on just showing a list with all the posts. First start with the model.

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

We have a `Post` model to represent our blog's data. Very simple, just a post with a title and some content, written by a certain user at a certain time.
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

Now that we have our data defined, time to display it!

## blog/urls.py ##

    from django.conf.urls import url
    from . import views
    
    urlpatterns = [
        url( r'^$', views.listAll, name= 'listAll' ),
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
        <div>
            <a href="{% url 'listAll' %}">Home</a>
            {% block content %}{% endblock %}
        </div>
    </body>
    </html>

## blog/templates/blog/listAll.html ##

    {% extends 'blog/base.html' %}
    
    {% block content %}
        <h1>My Blog!</h1>
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

Time to apply all migrations to the database.

`python manage.py makemigrations`
`python manage.py migrate`

And start the server.

`python manage.py runserver`

We'll be adding blog posts through the django admin page, so for starters, lets create a superuser account.

`python manage.py createsuperuser`

Now just go to the `/admin/` url, click on the `add` button on the blog section to add a new post.

If you go back to the home page, you'll see a list with the titles of the posts you just added.
  
# Individual Post #
  
We need to be able to open individual blog posts, which is basically a page where all the post information is shown.

## blog/urls.py ##

    from django.conf.urls import url
    from . import views
    
    urlpatterns = [
        url( r'^$', views.listAll, name= 'listAll' ),
        url( r'^post/(?P<slug>[-\w]+)$', views.showPost, name= 'showPost' ),
    ]

The url will contain a post's `slug`, which is how we identify which post to show.
Notice that we're also giving names to the urls, so its easier to reference it in templates, as we'll see below.

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
        <h1>My Blog!</h1>
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

## blog/models.py ##

    class Category( models.Model ):
        name = models.CharField( max_length= 50, unique= True )
        slug = models.SlugField( max_length= 50, unique= True )
    
        def __str__(self):
            return self.name
    
    class Post( models.Model ):
        # (...)
        categories = models.ManyToManyField( Category )

        def __str__(self):
            return self.title

We add a new model for a category, it has a name and a slug (to be used as the url for a list of all posts from that category).

On the `Post` model, we need to add a `categories` field. A post can have multiple categories, and each category can be in any number of posts, so what we need is a `ManyToManyField` property. 

We've added as well a `__str__()` method to the models, useful for example when choosing the categories of a new post in the admin page.

Since we changed the models, we'll need to update our migrations.

`python manage.py makemigrations`
`python manage.py migrate`

Now lets update our admin code, so we can easily add categories through the admin page.

## blog/admin.py ##

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

The category's `slug` gets automatically added based on the name (similar to how it happens on the `Post` model). We're also adding a way to filter the posts per category.

If you had some posts added already, make sure to add some categories to them, through the django admin page.

## blog/templates/blog/showPost.html ##

    {% extends 'blog/base.html' %}
    
    {% block content %}
        <h1>{{ post.title }} - by {{ post.author }} on {{ post.date_added }}</h1>
        <h2>
            Categories:
            {% for category in post.categories.all %}
                {{ category.name }}
            {% endfor %}
        </h2>
        <p>{{ post.content }}</p>
    
        <a href="{% url 'listAll' %}">Back</a>
    {% endblock %}

We can show the categories of each post in the template.

# Category List #

It can be useful to show only the posts from a certain category, so lets take care of that. By now you should already have an idea on how this works, we need to set up an url, add a view and a template.

## blog/urls.py ##

    urlpatterns = [
        # (...)
        url( r'^category/(?P<slug>[-\w]+)$', views.showCategory, name= 'showCategory' ),
    ]

## blog/views.py ##

    from .models import Post, Category
    # (...)
    
    def showCategory( request, slug ):
        category = get_object_or_404( Category, slug= slug )
    
        context = {
            'category': category,
            'posts': category.post_set.all()
        }
    
        return render( request, 'blog/showCategory.html', context )

## blog/templates/blog/showCategory.html ##

    {% extends 'blog/base.html' %}
    
    {% block content %}
        <h1>{{ category.name }}</h1>
        {% if posts %}
            <ul>
                {% for post in posts %}
                    <li><a href="{% url 'showPost' post.slug %}">{{ post.title }}</a></li>
                {% endfor %}
            </ul>
        {% else %}
            <p>No posts yet.</p>
        {% endif %}
    {% endblock %}

We'll also add a link to the category page, from the post page.

## blog/templates/blog/showPost.html ##

    {% extends 'blog/base.html' %}
    
    {% block content %}
        <h1>{{ post.title }} - by {{ post.author }} on {{ post.date_added }}</h1>
        <h2>
            Categories:
            {% for category in post.categories.all %}
                <a href="{% url 'showCategory' category.slug %}">{{ category.name }}</a>
            {% endfor %}
        </h2>
        <p>{{ post.content }}</p>
    
        <a href="{% url 'listAll' %}">Back</a>
    {% endblock %}

We use the `slug` as a way to build the link to the category page (similar to what we're doing for the posts).

# Category Menu #

It can also be nice to have a list of all the categories visible at all times, for example as a column in the right side of the page. To do that, we'll need to change the `base.html` template.

## blog/templates/blog/base.html ##

    {% load static %}
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8" />
            <title>Blog</title>
            <link rel="stylesheet" href="{% static 'blog/style.css' %}" />
        </head>
    <body>
        <div>
            <a href="{% url 'listAll' %}">Home</a>
            {% block content %}{% endblock %}
        </div>
        <div>
            {% if categories %}
                <h2>Categories</h2>
                <ul>
                    {% for category in categories %}
                        <li><a href="{% url 'showCategory' category.slug %}">{{ category.name }}</a> {{ category.post_set.count }}x</li>
                    {% endfor %}
                </ul>
            {% endif %}
        </div>
    </body>
    </html>

We add a list with all the categories available, and with a value next to it that tells how many posts of that particular category are there.

## blog/static/blog/style.css ##

    body {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }

We'll also divide our blog in two columns, with the left side having the content, and the right side the categories list. You're free to improve the styling as you see fit.

## blog/views.py ##

    from django.db.models import Count
    # (...)
    
    def getSortedCategories():
        return Category.objects.annotate( count= Count( 'post' ) ).order_by( '-count' )
    
    def listAll( request ):
        context = {
            'categories': getSortedCategories(),
            'posts': Post.objects.all()
        }
    
        return render( request, 'blog/listAll.html', context )
    # (...)

We get the categories sorted by the number of posts per category, and then we add to the context on all the views (only showing the `listAll()` here).

# Search #

It can also be useful to have a search functionality, here's an example on how that could be done.

We want it to be available in all pages, so we'll add it to the `base.html` template as well.

## blog/urls.py ##

    urlpatterns = [
        # (...)
        url( r'^search$', views.search, name= 'search' ),
    ]

## blog/views.py ##

    # (...)
    
    def search( request ):
        query = request.POST.get( 'search' )
        context = {
            'categories': getSortedCategories(),
            'query': query
        }
    
        if query and (4 <= len(query) <= 20):
            context[ 'posts' ] = Post.objects.filter( title__icontains= query )
    
        else:
            context[ 'message' ] = 'Query needs to be between 4 and 20 characters.'
    
        return render( request, 'blog/search.html', context )

Here we're only accepting queries between 4 and 20 characters, and will show a message if the query doesn't fall in that range.

## blog/templates/blog/base.html ##

    <!-- (...) -->
    <div>
        {% if categories %}
            <h2>Categories</h2>
            <ul>
                {% for category in categories %}
                    <li><a href="{% url 'showCategory' category.slug %}">{{ category.name }}</a> {{ category.post_set.count }}x</li>
                {% endfor %}
            </ul>
        {% endif %}
        <form action="{% url 'search' %}" method="post">
            {% csrf_token %}
            <input name="search" type="text" maxlength="20" />
            <button type="submit">🔍</button>
        </form>
    </div>

We add the search elements on the right column (below the categories list).

## blog/templates/blog/search.html ##

    {% extends 'blog/base.html' %}
    
    {% block content %}
        <h1>Searched for: {{ query }}</h1>
    
        {% if message %}
            <p>{{ message }}</p>
        {% endif %}
    
        {% if posts %}
            <ul>
                {% for post in posts %}
                    <li><a href="{% url 'showPost' post.slug %}">{{ post.title }}</a></li>
                {% endfor %}
            </ul>
        {% else %}
            <p>No results.</p>
        {% endif %}
    {% endblock %}

In the search template, we show what was the query given, and any given error message if available. Beyond that, its just a simple list of posts that match the search.

# Done! #

Voila! We have ourselves a blog. 

This is obviously a very crude blog, but hopefully it can give you some ideas to get you started on building your own. From here you can improve the styling of blog, and add any other feature you might need.
