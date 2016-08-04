from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category( models.Model ):

    name = models.CharField( max_length= 50, unique= True )
    slug = models.SlugField( max_length= 50, unique= True )

    def __str__(self):
        return self.name


class Post( models.Model ):

    author = models.ForeignKey( User )
    title = models.CharField( max_length= 100 )
    slug = models.SlugField( max_length= 100, unique= True )
    content = models.TextField()
    date_added = models.DateTimeField( default= timezone.now )
    categories = models.ManyToManyField( Category )

    class Meta:
        ordering = ( '-date_added', )

    def __str__(self):
        return self.title
