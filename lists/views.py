from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError

from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    items_list = List.objects.get(id=list_id)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data=request.POST)

        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=items_list)
            return redirect(items_list)

    return render(
        request,
        'list.html',
        {'list': items_list, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)

    if form.is_valid():
        items_list = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=items_list)

        return redirect(items_list)

    return render(request, 'home.html', {'form': form})
