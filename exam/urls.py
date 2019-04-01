from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^teacher/', views.teacher),
    url(r'^edit/', views.edit),

    url(r'^fillblank/', views.fillblank_train),
    url(r'^training/', views.training),
    url(r'^updateQuestion', views.update_question),
    url(r'^updateAnswer', views.update_answer),
    url(r'^updatePoints', views.update_points),
    url(r'^updateScore', views.update_score),

    url(r'^shortAnswer/', views.short_answer_train),
    url(r'^updateBranch', views.update_branch),
    url(r'^saveTraining', views.saveTraining),

    url(r'^addQusetion', views.add_question),

    url(r'^test/', views.test),
    url(r'^getConcepts/', views.get_concepts)
]
