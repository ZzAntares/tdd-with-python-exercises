from django.shortcuts import render
from lists.models import Item


def home_page(request):
    # TODO: Avoid saving empty items in every request
    item = Item()
    item.text = request.POST.get('item_text', '')
    item.save()

    return render(
        request,
        'home.html',
        {'new_item_text': request.POST.get('item_text', '')})
