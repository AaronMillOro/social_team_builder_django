#from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.urls import static

from . import views

app_name = 'teams'


urlpatterns = [
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^sign_in/$', views.sign_in, name='sign_in'),
    url(r'^sign_out/$', views.sign_out, name='sign_out'),

    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile_edit/$', views.profile_edit, name='profile_edit'),
    url(r'^add_skill/$', views.add_skills, name='add_skills'),

    url(r'^projects/$', views.my_projects, name='my_projects'),
    url(r'^projects_create/$', views.create_project, name='create_project'),

    url(r'^applications/$', views.applications, name='applications'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
