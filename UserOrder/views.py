from django.shortcuts import render, HttpResponse, redirect
from RestaurantEvent.models import *
from UserOrder.models import *
from UserLogin.models import *
from RestaurantItem.models import *
from django.contrib import messages
import math

debug = False

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
        errors = OrderQuantity.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags = key)
            return redirect(f"/user/order/{eventID}/new")
        else:
            user = User.objects.get(id=request.session["userID"])
            event = Event.objects.get(id=eventID)
            order = Order.objects.create(user = user, event=event, status="Received", total_price=0)
            for item_id, quantity in request.POST.items():
                if item_id != "csrfmiddlewaretoken":
                    if int(quantity) > 0:
                        OrderQuantity.objects.create(item=Item.objects.get(id=int(item_id)), order = order, quantity= quantity)
            #calculate up all order items
            total = 0
            items = order.quantities.all()
            for item in items:
                total += item.item.item_price * item.quantity
            order.total_price = total
            order.save()
            return redirect(f"/user/order/{event.id}/{order.id}/review")
    else:
        return redirect("/")


#Path is /user/order/<int:eventID>/<int:orderID>/review
def reviewOrder(request, eventID, orderID):
    if debug:
        request.session["userID"] = 1
    order = Order.objects.get(id=orderID)
    event = Event.objects.get(id=eventID)
    user = User.objects.get(id=request.session["userID"])
    #Calculate total
    total = 0
    for item in order.quantities.all():
        total += item.item.item_price * item.quantity
    context = {
        "event": event,
        "order": order,
        "itemQuantities": order.quantities.all(),
        "restaurant": event.restaurant,
        "user": user,
        "total": '{:.2f}'.format(total)
    }
    return render(request, "reviewOrder.html", context)

#Path is /user/order/<int:eventID>/<int:orderID>/change
def changeOrder(request, eventID, orderID):
    order = Order.objects.get(id=orderID)
    order.delete()
    return redirect(f"/user/order/{eventID}/new")

#Path is /user/order/<int:eventID>/<int:orderID>/status/<string:status/update
def updateOrderStatus(request,eventID, orderID, status):
    if "restaurantID" in request.session:
        event = Event.objects.get(id=eventID)
        #Make sure restaurant that is logged in is the same as the restaurant of the event
        if request.session["restaurantID"] == event.restaurant.id:
            #update status
            order = Order.objects.get(id=orderID)
            order.status = status
            order.save()
            return HttpResponse("Successfully updated order")
    else:
        return redirect("/")