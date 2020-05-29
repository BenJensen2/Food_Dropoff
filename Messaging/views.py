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


def orderCancel(request, orderID):
    # cancel order
    if request.method == 'GET' and not request.is_ajax():
        order = Order.objects.filter(id=orderID)
        if order:
            order = Order.objects.get(id=orderID)
            event = order.event_id
            if 'restaurantID' in request.session:
                rid = Order.objects.get(id=orderID).event.restaurant_id
                if rid == request.session['restaurantID'] and (order.status == 'Received' or order.status == 'Confirmed'):
                    order.status = 'Cancelled'
                    order.save()
                    return redirect(f'/event/{event}')
            elif 'userID' in request.session:
                uid = Order.objects.get(id=orderID).user_id
                if uid == request.session['userID'] and order.status == 'Received':
                    order.status = 'Cancelled'
                    order.save()
                    return redirect(f'/users')
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
                    Message.objects.create(order_id=orderID,sent_by='restaurant',message=f'{order.event.restaurant.restaurant_name} has confirmed order {order.id}.')
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
                    return render(request,'user-msgcontent.html', context)
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
                    return render(request,'user-msgcontent.html', context)
    return redirect('/')