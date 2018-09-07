from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^teacher/', views.teacher),
    url(r'^edit/', views.edit),
    url(r'^add/', views.add),
    url(r'^training/', views.training),
    url(r'^updateAnswer', views.update_answer)
]
