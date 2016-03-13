from django.shortcuts import redirect, render
from fridges.models import Store

def home_page(request):
    if request.method == 'POST':
        Store.objects.create(text=request.POST['store_text'])
        return redirect('/stores/the-only-store/')

    stores = Store.objects.all()
    return render(request, 'home.html', {'stores': stores})

def view_store(request):
    stores = Store.objects.all()
    return render(request, 'store.html', {'stores': stores})

def new_store(request):
    store = Store.objects.create()
    Item.objects.create(text=request.POST['item_text'], store=store)
    return redirect('/stores/the-only-store/')