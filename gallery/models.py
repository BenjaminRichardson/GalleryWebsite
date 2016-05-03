from django.db import models
import os
import datetime
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.sites.models import Site

def group_path(instance, filename):
	# make directory if not there
	path = settings.MEDIA_URL+ str(instance.parent.pk)
	timestamp_filename = '-'.join([str(datetime.datetime.now()), filename])
	full_os_path = os.path.join(settings.BASE_DIR,settings.MEDIA_URL_RAW,str(instance.parent.pk))
	print(full_os_path)
	if os.path.exists(full_os_path) is False:
		os.makedirs(full_os_path)
	#save with current time and old filename
	return str(instance.parent.pk)+'/'+timestamp_filename

# Create your models here.

class Group(models.Model):
	display_name 	= models.CharField(max_length=255)
	parent 			= models.ForeignKey(
						'self',
						on_delete=models.CASCADE,
						null=True, #null indicates top level group
						blank=True
					)
	description		= models.TextField(null=True,blank=True)

	class Meta:
		order_with_respect_to = 'parent'

	def swappable(self,swap_group):
		return swap_group.parent == self.parent

	def swap_order(self, swap_group):
		if type(swap_group) == type(self) and swap_group.parent == self.parent:
			temp_position = swap_group._order
			swap_group._order = self._order
			self._order = temp_position
			self.save()
			swap_group.save()

	def __str__(self):
		return self.display_name

class Gallery_Item(models.Model):
	display_name 	= models.CharField(max_length=255)
	parent	 		= models.ForeignKey(
						Group,
						on_delete=models.CASCADE
					)
	image		 	= models.ImageField(upload_to=group_path,null=True)
	thumbnail		= ImageSpecField(source='image',
						processors=[ResizeToFill(400,400)],
						format='JPEG',
						options={'quality':70}
					)
	description		= models.TextField(null=True,blank=True)

	class Meta:
		order_with_respect_to = 'parent'

	def swappable(self,swap_group):
		return swap_group.parent == self.parent

	def swap_order(self, swap_group):
		if type(swap_group) == type(self) and swap_group.parent == self.parent:
			temp_position = swap_group._order
			swap_group._order = self._order
			self._order = temp_position
			self.save()
			swap_group.save()

	def __str__(self):
		return self.display_name

class Site_Info(models.Model):
	site = models.OneToOneField(Site)
	display_name = models.CharField(max_length=255)
	body  	= models.TextField(blank=True,null=True)