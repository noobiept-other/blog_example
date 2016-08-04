from django.conf.urls import url
from . import views


urlpatterns = [
    url( r'^$', views.listAll, name= 'listAll' ),
    url( r'^post/(?P<slug>[-\w]+)$', views.showPost, name= 'showPost' ),
    url( r'^category/(?P<slug>[-\w]+)$', views.showCategory, name= 'showCategory' ),
    url( r'^search$', views.search, name= 'search' ),
]
