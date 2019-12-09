from django.urls import include, path
from django.conf.urls import url
from . import views
from camp_reg import settings
from django.conf.urls.static import static


urlpatterns = [
    # path()
    path(r'', views.welcome, name='welcome'),
    url(r'^base_signup/$', views.base_signup, name='base_signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login/<user>/', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/<child>$', views.register, name='register'),
    url(r'^home/$', views.home, name='home'),
    url(r'^parent_details/$', views.parent_details, name='parent_details'),
    url(r'^view/$', views.view, name='view'),
    url(r'^edit_student/$', views.edit_student, name='edit_student'),
    url(r'^list/$', views.list, name='list'),
    url(r'^router/$', views.router, name='router'),
    url(r'^download_all/$', views.download_all, name='download_all'),
    url(r'^student/$', views.student, name='student'),
    url(r'^download_resume/$', views.download_resume, name='download_resume'),
    url(r'^reset/$', views.reset, name='reset'),
    url('^', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)