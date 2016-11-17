from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    items_list = List.objects.get(id=list_id)

    return render(request, 'list.html', {'list': items_list})


def new_list(request):
    items_list = List.objects.create()
    item = Item(text=request.POST['item_text'], list=items_list)

    try:
        item.full_clean()
        item.save()
    except ValidationError:
        items_list.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})

    return redirect('/lists/{}/'.format(items_list.id))


def add_item(request, list_id):
    items_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=items_list)

    return redirect('/lists/{}/'.format(items_list.id))
