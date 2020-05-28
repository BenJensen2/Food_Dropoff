from django.shortcuts import render, HttpResponse, redirect
from .models import Menu, Item
from RestaurantLogin.models import *

debug = True

def index(request):
    context = {
        'menus' : Menu.objects.all()
    }
    return render(request,'menu_list.html',context)

#Path is /menu/new
def newMenu(request):
    if debug:
        request.session["restaurantID"] = 1
    if "restaurantID" in request.session:
        restaurant = Restaurant.objects.get(id=request.session["restaurantID"])
        #If restaurant doesn't already have a menu create one by default
        if len(restaurant.menus.all()) < 1:
            Menu.objects.create(name="Default", restaurant=restaurant)
        menu = restaurant.menus.all().first()
        context = {
            "restaurant": restaurant,
            "menu": menu
        }
        return render(request, "createMenu.html", context)
    else:
        return redirect("/")
    
#Path is /menu/new/addItem
def addItem(request):
    if debug:
        request.session["restaurantID"] = 1
    if "restaurantID" in request.session:
        restaurant = Restaurant.objects.get(id=request.session["restaurantID"])
        #Add new item to the menu then redirect to the menu creation page
        menu = Menu.objects.get(id = request.POST["menuID"])
        item = Item.objects.create(item_title = request.POST["item"], item_description = request.POST["description"], item_price = request.POST["price"], restaurant = restaurant)
        menu.items.add(item)
        return redirect("/menu/new")
    else:
        return redirect("/")

def create(request):
    Menu.objects.create(
        name=request.POST['name']
    )
    return redirect('/restaurant_menu')