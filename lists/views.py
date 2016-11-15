from django.shortcuts import redirect, render
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    items_list = List.objects.get(id=list_id)

    return render(request, 'list.html', {'list': items_list})


def new_list(request):
    items_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=items_list)

    return redirect('/lists/{}/'.format(items_list.id))


def add_item(request, list_id):
    items_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=items_list)

    return redirect('/lists/{}/'.format(items_list.id))
