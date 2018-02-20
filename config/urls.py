from django.contrib import admin
from django.conf.urls import url, include
from theroom import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^vip/', views.theroom),
    url(r'', views.index),
]
