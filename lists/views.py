from django.shortcuts import redirect, render
from lists.models import Item


def home_page(request):
    new_item_text = request.POST.get('item_text', '')

    if request.method == 'POST':
        Item.objects.create(text=new_item_text)
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
