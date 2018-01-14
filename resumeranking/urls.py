from django.conf.urls import url
from . import views

urlpatterns=[
    #url(r'^', views.index, name='index'),
    url(r'^index2/', views.index2, name='index3'),
    url(r'^choices/', views.choices, name='choices'),
    url(r'^$', views.index,name='index'),
    url(r'^logout/', views.logout,name='logout'),
    ]