from django.shortcuts import redirect, render
from fridges.models import Store, Item

def home_page(request):
    if request.method == 'POST':
        Store.objects.create(text=request.POST['store_text'])
        store = Store.objects.last()
        return redirect('/stores/%d/' % (store.id))

    stores = Store.objects.all()
    return render(request, 'home.html', {'stores': stores})

def view_store(request, store_id):
    store = Store.objects.get(id=store_id)
    return render(request, 'store.html', {'store': store})

def new_store(request):
    store = Store.objects.create()
    Item.objects.create(text=request.POST['item_text'], store=store)
    return redirect('/stores/%d/' % (store.id))

def add_item(request, store_id):
    store = Store.objects.get(id=store_id)
    Item.objects.create(text=request.POST['item_text'], store=store)
    return redirect('/stores/%d/' % (store.id))