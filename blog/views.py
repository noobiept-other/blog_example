from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Post, Category


def getSortedCategories():
    return Category.objects.annotate( count= Count( 'post' ) ).order_by( '-count' )


def listAll( request ):
    context = {
        'categories': getSortedCategories(),
        'posts': Post.objects.all()
    }

    return render( request, 'blog/listAll.html', context )


def showPost( request, slug ):
    context = {
        'categories': getSortedCategories(),
        'post': get_object_or_404( Post, slug= slug )
    }

    return render( request, 'blog/showPost.html', context )


def showCategory( request, slug ):
    category = get_object_or_404( Category, slug= slug )

    context = {
        'categories': getSortedCategories(),
        'category': category,
        'posts': category.post_set.all()
    }

    return render( request, 'blog/showCategory.html', context )


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
