from django.conf.urls import patterns, url

from myapp import views

urlpatterns = patterns('',
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^check_password/$', views.check_password, name='check_password'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^temp/$',views.temp, name='temp'),
    url(r'^get_list_files/$',views.get_list_files, name='get_list_files'),
    url(r'^checkForUpdates/$',views.checkForUpdates, name='checkForUpdates'),
	url(r'^pull_file/$',views.pull_file, name='pull_file'),
	url(r'^deleteFile/$',views.deleteFile, name='deleteFile'),
	)