from django.db import models
import os

def group_path(instance, filename):
	# make directory if not there

	# detect if file with same name is saved

		# if yes, search for '-#' at end, and return name with number incremented by one
		# if no, return path and already existant filename

# Create your models here.
class Group(models.Model):
	display_name 	= models.CharField(max_length=255)
	parent 			= models.ForeignKey(
						Group,
						on_delete=models.CASCADE,
						null=True #null indicates top level group
					)
	order			= models.SmallIntegerField

class Gallery_Item(models.Model):
	group_id	= models.ForeignKey(
					Group,
					on_delete=models.CASCADE
				)
	order		= models.SmallIntegerField
	image		= models.ImageField(upload_to=group_path)

