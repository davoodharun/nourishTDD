from django.shortcuts import redirect, render
from fridges.models import Store

def home_page(request):
    if request.method == 'POST':
        Store.objects.create(text=request.POST['item_text'])
        return redirect('/')

    stores = Store.objects.all()
    return render(request, 'home.html', {'stores': stores})
