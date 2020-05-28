from django.shortcuts import render, HttpResponse, redirect
from RestaurantEvent.models import *
from UserOrder.models import *
from UserLogin.models import *
from RestaurantItem.models import *
import math

debug = True

def index(request):
    return HttpResponse('Works')

#Path is /user/order/<int:eventID>/new
def newOrder(request, eventID):
    event = Event.objects.get(id=eventID)
    context = {
        "event": event,
        "menu": event.menu.items.all(),
        "restaurant": event.restaurant
    }
    return render(request, "createOrder.html", context)

#Path is /user/order/<int:eventID>/storeOrder
def storeOrder(request, eventID):
    if debug:
        request.session["userID"] = 1
    if "userID" in request.session:
        user = User.objects.get(id=request.session["userID"])
        event = Event.objects.get(id=eventID)
        order = Order.objects.create(user = user, event=event, status="Unconfirmed")
        for item_id, quantity in request.POST.items():
            if item_id != "csrfmiddlewaretoken":
                if int(quantity) > 0:
                    OrderQuantity.objects.create(item=Item.objects.get(id=int(item_id)), order = order, quantity= quantity)
        return redirect(f"/user/order/{event.id}/{order.id}/review")
    else:
        return redirect("/")

#Path is /user/order/<int:eventID>/<int:orderID>/review
def reviewOrder(request, eventID, orderID):
    order = Order.objects.get(id=orderID)
    event = Event.objects.get(id=eventID)
    context = {
        "event": event,
        "order": order,
        "itemQuantities": order.quantities.all(),
        "restaurant": event.restaurant
    }
    return render(request, "reviewOrder.html", context)