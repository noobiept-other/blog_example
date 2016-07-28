from django.shortcuts import render
from .models import Post


def listAll( request ):
    context = {
        'posts': Post.objects.all()
    }

    return render( request, 'blog/listAll.html', context )
