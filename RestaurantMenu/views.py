from django.shortcuts import render, HttpResponse, redirect
from .models import Menu, Item
from RestaurantLogin.models import *
from django.http import JsonResponse

debug = False

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
        return redirect(f"/menu/{menu.id}/content")
    else:
        return redirect("/")

#Path is /menu/new/<int:itemID>/removeItem
def removeItem(request, itemID):
    if debug:
        request.session["restaurantID"] = 1
    if "restaurantID" in request.session:
        menu = Restaurant.objects.get(id=request.session["restaurantID"]).menus.first()
        item = Item.objects.get(id=itemID)
        item.delete()
        return redirect(f"/menu/{menu.id}/content")
    else:
        return redirect("/")

def create(request):
    Menu.objects.create(
        name=request.POST['name']
    )
    return redirect('/restaurant_menu')


def validateRID(request, restaurantID):
    # if "userID" in request.session and request.is_ajax():
    restaurant = Restaurant.objects.filter(id=restaurantID)
    if restaurant:
        return JsonResponse({"valid":True}, status = 200)
    else:
        return JsonResponse({"valid":False}, status = 200)
    # return JsonResponse({"valid":False}, status = 200)

#path is /menu/<int:menuID>/content for Ajax getting menu items
def menuContent(request, menuID):
    restaurant = Restaurant.objects.get(id=request.session["restaurantID"])
    menu = restaurant.menus.first()
    context = {
        "menu": menu
    }
    return render(request, "menuContent.html", context)

