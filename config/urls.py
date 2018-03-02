from django.contrib import admin
from django.conf.urls import url, include
from theroom import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^the_website/', views.the_website),
    url(r'^exit/', views.exit),
    url(r'^goodbye', views.goodbye),
    url(r'^$', views.index),
]