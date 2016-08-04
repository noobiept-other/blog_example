from django.shortcuts import render, get_object_or_404
from .models import Post, Category


def listAll( request ):
    context = {
        'posts': Post.objects.all()
    }

    return render( request, 'blog/listAll.html', context )


def showPost( request, slug ):
    context = {
        'post': get_object_or_404( Post, slug= slug )
    }

    return render( request, 'blog/showPost.html', context )


def showCategory( request, slug ):
    category = get_object_or_404( Category, slug= slug )

    context = {
        'category': category,
        'posts': category.post_set.all()
    }

    return render( request, 'blog/showCategory.html', context )
