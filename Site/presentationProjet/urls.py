
from django.urls import path

from . import views # import views so we can use them in urls.
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('Etude', views.etude1, name="etude"),
    path('LDA', views.detailLDA, name="LDA"),
    path('Tweet', csrf_exempt(views.receivetweet), name="tweet"),
]