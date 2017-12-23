from django.conf.urls import url, include
from . import views

app_name = 'mcq'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create-paper/$', views.create_paper, name='create-paper'),
    url(r'^create-question/$', views.create_question, name='create-question'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^papers/(?P<paper_pk>[0-9]+)/$', views.paper, name='paper'),
    url(r'^check/(?P<paper_pk>[0-9]+)/$', views.check, name='check'),
    #url('^', include('django.contrib.auth.urls')),
    url(r'^send-mails/$', views.send_mails, name='send-mails'),
    url(r'^edit-question/(?P<question_pk>[0-9]+)/$', views.edit_question, name='edit-question'),
    url(r'^delete-question/(?P<question_pk>[0-9]+)/$', views.delete_question, name='delete-question'),
    url(r'^delete-paper/(?P<paper_pk>[0-9]+)/$', views.delete_paper, name='delete-paper'),
]

