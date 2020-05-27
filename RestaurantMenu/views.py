from django.shortcuts import render, HttpResponse, redirect
from .models import Menu, Item

def index(request):
    context = {
        'menus' : Menu.objects.all()
    }
    return render(request,'menu_list.html',context)

def create(request):
    Menu.objects.create(
        name=request.POST['name']
    )
    return redirect('/restaurant_menu')