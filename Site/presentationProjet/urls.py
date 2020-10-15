
from django.urls import path

from . import views # import views so we can use them in urls.


urlpatterns = [
    path('Etude1', views.etude1, name="etude"),
]