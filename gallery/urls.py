from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^/?$', views.top_level_group, name='top level groups'),
	url(r'^[0-9]*/?$', views.find_group_by_id, name='group by id'),
]