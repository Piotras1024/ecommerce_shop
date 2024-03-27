from django.shortcuts import render

# Create your views here.


def store(request):
    return render(request, 'store_clothes/store.html')
