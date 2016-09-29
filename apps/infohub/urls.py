from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'adminportal$', views.adminPortal, name = 'adminportal'),
    url(r'profile$', views.show_profile, name = 'show_profile'),
    url(r'profile/set$', views.set_preferences, name = 'set_preferences'),
    url(r'getinfo$', views.getInfo, name = 'getInfo')
]
