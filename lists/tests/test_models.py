from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import List, Item


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        items_list = List()
        items_list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = items_list
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = items_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, items_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, items_list)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, items_list)

    def test_can_not_save_empty_list_items(self):
        items_list = List.objects.create()
        item = Item(list=items_list, text='')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
