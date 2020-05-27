from django.shortcuts import render, HttpResponse
from RestaurantEvent.models import *

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
    pass