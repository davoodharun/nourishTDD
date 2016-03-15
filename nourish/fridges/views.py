from django.shortcuts import redirect, render
from fridges.models import Fridge, Item

def home_page(request):
    if request.method == 'POST':
        Fridge.objects.create(text=request.POST['fridge_text'])
        fridge = Fridge.objects.last()
        return redirect('/fridges/%d/' % (fridge.id))

    fridges = Fridge.objects.all()
    return render(request, 'home.html', {'fridges': fridges})

def view_fridge(request, fridge_id):
    fridge = Fridge.objects.get(id=fridge_id)
    return render(request, 'fridge.html', {'fridge': fridge})

def new_fridge(request):
    fridge = Fridge.objects.create(text=request.POST['fridge_text'])
    return redirect('/fridges/%d/' % (fridge.id))

def add_item(request, fridge_id):
    fridge = Fridge.objects.get(id=fridge_id)
    Item.objects.create(text=request.POST['item_text'], fridge=fridge)
    return redirect('/fridges/%d/' % (fridge.id))