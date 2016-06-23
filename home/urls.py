from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = (
    url(r'^$', views.index, name='index'),
    url(r'^news/', views.news, name='news'),
    url(r'^about/', views.about, name='about'),
    url(r'^resources/', views.resources, name='resources'),
    url(r'^faq/', views.faq, name='faq'),
)
