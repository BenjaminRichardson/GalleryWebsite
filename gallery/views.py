from django.shortcuts import render
from django.core.urlresolvers import resolve
from django.http import Http404
from gallery.models import Group,Gallery_Item
from django.contrib.sites.models import Site

# Create your views here.
def index(request):
	current_url = request.path_info
	current_group_id = current_url.split('/')[-1]
	#if Group.objects.filter(id = current_group_id).count() == 0:
		#404
		#str('hello')
	parents = list(Group.objects.all().filter(parent=None))
	context = {'parents':parents,'current':current_group_id}
	return render(request,'gallery/display_group_template.html',context)

def top_level_group(request):
	top_groups = list(Group.objects.all().filter(parent=None))
	site_info = Site.objects.get_current().site_info
	context = {'top_groups':top_groups,'site_info':site_info}
	return render(request,'gallery/display_top_level_group_template.html',context)

def find_group_by_id(request):
	url = request.path_info
	group_id = int(url.split('/')[2])
	group = Group.objects.all().filter(id=group_id)
	if len( group ) != 1:
		return HttpResponseNotFound('Error retrieving that group')
	context = {'group':group[0],"url":url}
	return render(request, 'gallery/display_group_template.html', context)


def admin(request):
	pass
	