from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^teacher/', views.teacher),
    url(r'^edit/', views.edit),
]
