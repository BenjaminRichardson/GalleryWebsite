from django.contrib import admin
from django.contrib import messages

# Register your models here.
from .models import Group,Gallery_Item,Site_Info

def swap_order(modeladmin, request, queryset):
	swap_order.short_description = "Swap two items"
	if len(queryset) == 2:
		first_orderable = queryset[0]
		second_orderable = queryset[1]
		if first_orderable.swappable(second_orderable):
			first_orderable.swap_order(second_orderable)
		else:
			messages.error(request,"The two items must have the same parent")
	else:
		messages.error(request,"Please select two items to swap")

class GroupAdmin(admin.ModelAdmin):
	list_display = ('display_name','parent','_order')
	ordering = ['_order']
	actions = [swap_order]

class Gallery_ItemAdmin(admin.ModelAdmin):
	list_display = ('display_name','image','parent','_order')
	ordering = ['_order']
	actions = [swap_order]

class Site_Info_admin(admin.ModelAdmin):
	list_display = ['display_name']

admin.site.register(Group, GroupAdmin)
admin.site.register(Gallery_Item, Gallery_ItemAdmin)
admin.site.register(Site_Info, Site_Info_admin)

