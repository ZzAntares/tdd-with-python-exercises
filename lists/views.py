from django.shortcuts import redirect, render

from lists.forms import ExistingListItemForm, ItemForm
from lists.models import List


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    items_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=items_list)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=items_list, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect(items_list)

    return render(
        request,
        'list.html',
        {'list': items_list, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)

    if form.is_valid():
        items_list = List.objects.create()
        form.save(for_list=items_list)

        return redirect(items_list)

    return render(request, 'home.html', {'form': form})
