from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import List, Item


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()

        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        items_list = List.objects.create()
        item = Item()
        item.list = items_list
        item.save()

        self.assertIn(item, items_list.item_set.all())

    def test_can_not_save_empty_list_items(self):
        items_list = List.objects.create()
        item = Item(list=items_list, text='')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        items_list = List.objects.create()
        Item.objects.create(list=items_list, text='bla')

        with self.assertRaises(ValidationError):
            item = Item(list=items_list, text='bla')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # Should work


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        items_list = List.objects.create()

        self.assertEqual(
            items_list.get_absolute_url(),
            '/lists/{}/'.format(items_list.id))
