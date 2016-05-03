from django.test import TestCase
from .models import Group, Gallery_Item
from django.utils import timezone
# Create your tests here.
class GroupTests(TestCase):

	def setUp(self):
		self.top_group_name = '-'.join(['test','top',str(timezone.now())])
		self.sub_group_name_1 = '-'.join(['test','sub','1',str(timezone.now())])
		self.sub_group_name_2 = '-'.join(['test','sub','2',str(timezone.now())])
		#add top level group
		g = Group.objects.create(display_name=self.top_group_name,parent=None)
		Group.objects.create(display_name=self.sub_group_name_1,parent=g)
		Group.objects.create(display_name=self.sub_group_name_2,parent=g)
	
	#added top level group has correct order
	def test_newly_created_top_level_position(self):
		topLevelGroups = Group.objects.all().filter(parent=None)
		self.assertTrue(topLevelGroups) #some top level elements exist
		lastGroup = topLevelGroups.reverse()[0]
		justCreatedGroup = Group.objects.get(display_name=self.top_group_name)
		self.assertEqual(lastGroup,justCreatedGroup)

	#remove top level group
	def test_remove_newly_created_top_level(self):
		g = Group.objects.get(display_name=self.top_group_name)
		g.delete()
		self.assertNotIn(g,Group.objects.all().filter(parent=None))

	#added sub level group has correct order
	def test_newly_created_sub_position(self):
		topLevelGroup = Group.objects.get(display_name=self.top_group_name)
		subLevelGroups = Group.objects.all().filter(parent=topLevelGroup)
		self.assertTrue(subLevelGroups)
		#check correct order
		lastGroup = subLevelGroups.reverse()[0]
		secondLastGroup = subLevelGroups.reverse()[1]
		self.assertEqual(secondLastGroup,Group.objects.get(display_name=self.sub_group_name_1))
		self.assertEqual(lastGroup,Group.objects.get(display_name=self.sub_group_name_2))

	#remove sub group
	def test_remove_newly_created_top_level(self):
		g = Group.objects.get(display_name=self.top_group_name)
		h = Group.objects.get(display_name=self.sub_group_name_1)
		h.delete()
		self.assertNotIn(g,Group.objects.all().filter(parent=g))

	#add group, rename, delete
	def test_rename_group(self):
		new_name = '-'.join(['new','test','sub','1',str(timezone.now())])
		g = Group.objects.get(display_name=self.top_group_name)
		g.display_name = new_name
		g.save();
		self.assertIn(Group.objects.get(display_name=new_name),Group.objects.all().filter(parent=None))
		self.assertEqual(g,Group.objects.get(display_name=new_name))

	def test_swap_order(self):
		one = Group.objects.get(display_name=self.top_group_name)
		second_name = '-'.join(['2','test','top',str(timezone.now())])
		two = Group.objects.create(display_name=second_name,parent=None)
		third_name = '-'.join(['3','test','top',str(timezone.now())])
		three = Group.objects.create(display_name=third_name,parent=None)
		one.swap_order(three)
		all_top_level = Group.objects.all().filter(parent=None)
		self.assertEqual(all_top_level[0],three)
		self.assertEqual(all_top_level[1],two)
		self.assertEqual(all_top_level[2],one)