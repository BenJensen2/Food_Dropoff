from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import JsonResponse


# Create your views here.
def index(request):
    # redirect to welcome page
    return redirect('/')

def orderDetail(request, orderID):
    # display order detail
    order = Order.objects.filter(id=orderID)
    if order:
        if 'restaurantID' in request.session:
            rid = Order.objects.get(id=orderID).event.restaurant_id
            print(rid)
            print(request.session['restaurantID'])
            if rid == request.session['restaurantID']:
                order = Order.objects.get(id=orderID)
                running_total = 0
                for i in order.quantities.all():
                    running_total += i.quantity * i.item.item_price
                    print(running_total)

                context = {
                    'one_order': Order.objects.get(id=orderID),
                    'order_messages': Message.objects.filter(order_id=orderID).order_by('created_at'),
                    'order_sum': running_total,
                }
                return render(request,'restaurant-orderdetail.html', context)
        elif 'userID' in request.session:
            uid = Order.objects.get(id=orderID).user_id
            if uid == request.session['userID']:
                order = Order.objects.get(id=orderID)
                running_total = 0
                for i in order.quantities.all():
                    running_total += i.quantity * i.item.item_price

                context = {
                    'one_order': Order.objects.get(id=orderID),
                    'order_messages': Message.objects.filter(order_id=orderID).order_by('created_at'),
                    'order_sum': running_total,
                }
                return render(request,'user-orderdetail.html', context)
    return redirect('/')


def orderDelete(request, orderID):
    # cancel order
    if request.method == 'GET' and not request.is_ajax():
        order = Order.objects.filter(id=orderID)
        if order:
            order = Order.objects.get(id=orderID)
            event = order.event_id
            if 'restaurantID' in request.session:
                rid = Order.objects.get(id=orderID).event.restaurant_id
                if rid == request.session['restaurantID'] and (order.status == 'Received' or order.status == 'Confirmed'):
                    order.delete()
                    return redirect(f'/RestaurantEvent/{event}')
            elif 'userID' in request.session:
                uid = Order.objects.get(id=orderID).user_id
                if uid == request.session['userID'] and order.status == 'Received':
                    order.delete()
                    return redirect(f'/RestaurantEvent/{event}')
    return redirect('/')

def orderConfirm(request, orderID):
    # confirm order
    if request.method == 'GET' and  request.is_ajax():
        order = Order.objects.filter(id=orderID)
        if order:
            order = Order.objects.get(id=orderID)
            if 'restaurantID' in request.session:
                rid = Order.objects.get(id=orderID).event.restaurant_id
                if rid == request.session['restaurantID'] and (order.status == 'Received'):
                    order.status = 'Confirmed'
                    order.save()
                    Message.object.create(order_id=orderID,sent_by='restaurant',message=f'{order.event.restaurant.name} has confirmed order {order.id}.')
                    context = {
                        'one_order': Order.objects.get(id=orderID),
                    }
                    return render(request,'orderstatus.html', context)
    return redirect('/')

def loadMessage(request, orderID):
    #Render partial html
    if request.method == 'GET' and  request.is_ajax():
        order = Order.objects.filter(id=orderID)
        if order:
            order = Order.objects.get(id=orderID)
            if 'restaurantID' in request.session:
                rid = Order.objects.get(id=orderID).event.restaurant_id
                if rid == request.session['restaurantID']:
                    context = {
                        'one_order': Order.objects.get(id=orderID),
                        'order_messages': Message.objects.filter(order_id=orderID).order_by('created_at'),
                    }
                    return render(request,'restaurant-messages.html', context)
            elif 'userID' in request.session:
                uid = Order.objects.get(id=orderID).user_id
                if uid == request.session['userID']:
                    context = {
                        'one_order': Order.objects.get(id=orderID),
                        'order_messages': Message.objects.filter(order_id=orderID).order_by('created_at'),
                    }
                    return render(request,'user-messages.html', context)
    return redirect('/')

def refreshMessage(request, orderID):
    #Render partial html
    if request.method == 'GET' and  request.is_ajax():
        order = Order.objects.filter(id=orderID)
        if order:
            order = Order.objects.get(id=orderID)
            if 'restaurantID' in request.session:
                rid = Order.objects.get(id=orderID).event.restaurant_id
                if rid == request.session['restaurantID']:
                    context = {
                        'one_order': Order.objects.get(id=orderID),
                        'order_messages': Message.objects.filter(order_id=orderID).order_by('created_at'),
                    }
                    return render(request,'restaurant-msgcontent.html', context)
            elif 'userID' in request.session:
                uid = Order.objects.get(id=orderID).user_id
                if uid == request.session['userID']:
                    context = {
                        'one_order': Order.objects.get(id=orderID),
                        'order_messages': Message.objects.filter(order_id=orderID).order_by('created_at'),
                    }
                    return render(request,'user-messages.html', context)
    return redirect('/')

def sendMessage(request):
    #Process POST request for new message
    #Render partial html
    if request.method == 'POST' and  request.is_ajax():
        order = Order.objects.filter(id=request.POST['oid'])
        if order:
            order = Order.objects.get(id=request.POST['oid'])
            if 'restaurantID' in request.session:
                rid = Order.objects.get(id=request.POST['oid']).event.restaurant_id
                if rid == request.session['restaurantID'] and len(request.POST['message'])>0:
                    Message.objects.create(order_id=request.POST['oid'],sent_by='restaurant',message=request.POST['message'])
                    context = {
                        'one_order': Order.objects.get(id=request.POST['oid']),
                        'order_messages': Message.objects.filter(order_id=request.POST['oid']).order_by('created_at'),
                    }
                    return render(request,'restaurant-msgcontent.html', context)
            elif 'userID' in request.session:
                uid = Order.objects.get(id=request.POST['oid']).user_id
                if uid == request.session['userID'] and len(request.POST['message'])>0:
                    Message.objects.create(order_id=request.POST['oid'],sent_by='user',message=request.POST['message'])
                    context = {
                        'one_order': Order.objects.get(id=request.POST['oid']),
                        'order_messages': Message.objects.filter(order_id=request.POST['oid']).order_by('created_at'),
                    }
                    return render(request,'user-messages.html', context)
    return redirect('/')

    # Restaurants
    #     - [method] Render order detail page for restaurant - orderDetail
    #           - current oid in context
    #     - [method with ajax call] confirm order - orderConfirm
    #           - update record in order table
    #           - current oid in context
    #           - change status and button/link (confirm link should disappear)
    #     - [method] cancel order - orderDelete
    #           - delete record in order table
    #           - redirect to eventdetail
    #     - [jquery] open message window, reload with timer - loadMessage
    #           - load partial html into message div
    #     - [method with ajax call] send message to user - sendMessage
    #           - create new record in message table with sent_by='restaurant'
    #           - load partial html into message div

    # Users
    #     - [method] Render order detail page for User - orderDetail
    #           - current oid in context
    #     - [method] cancel order - orderDelete
    #           - delete record in order table
    #           - redirect to eventdetail
    #     - [jquery] open message window, reload with timer - loadMessage
    #           - load partial html into message div
    #     - [method with ajax call] send message to Restaurants - sendMessage
    #           - create new record in message table with sent_by='user'
    #           - load partial html into message div