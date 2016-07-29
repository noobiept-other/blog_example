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
