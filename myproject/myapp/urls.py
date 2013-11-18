from django.conf.urls import patterns, url

from myapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^check_password/$', views.check_password, name='check_password'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^upload/$', views.upload, name='upload')
)