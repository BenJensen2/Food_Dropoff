from django.shortcuts import render, HttpResponse, redirect
from RestaurantEvent.models import Event
from RestaurantMenu.models import Menu
from RestaurantLogin.models import Restaurant
from .models import User, UserManager
from django.contrib import messages
import bcrypt

def index(request):
    # render homepage
    return render(request,'homepage.html')

def users(request):
    if 'restaurantID' in request.session:
        restaurant = Restaurant.objects.filter(id=request.session['restaurantID'])
        if restaurant:
            return redirect('/restaurantlogin/welcome')
        else:
            request.session.flush()
            return redirect('/')
    elif 'userID' in request.session:
        user = User.objects.filter(id=request.session['userID'])
        if user:
            return redirect(f"/users/{request.session['userID']}")
        else:
            request.session.flush()
            return redirect('/')
    return render(request,'user_login.html')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value,extra_tags=key)
        return redirect('/users')
    else:
        user = User.objects.filter(email=request.POST['logemail'])[0]
        request.session['userID'] = user.id
        return redirect(f'/users/{user.id}')

def logout(request):
    request.session.flush()
    return redirect('/')

def register(request):
    return render(request,'user_registration.html')

def create(request):
    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value,extra_tags=key)
        return redirect('/users/register')
    else:
        
        password_encoded = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = password_encoded,
            phone_number = request.POST['phone_number']
        )
        request.session['userID'] = user.id

        return redirect(f'/users/{user.id}')

def user_info(request,user_id):
    if 'userID' in request.session:
        user = User.objects.get(id=user_id)
        orders1 = user.orders.all().filter(status="In Progress")
        orders2 = user.orders.all().filter(status="Unconfirmed")
        orders3 = user.orders.all().filter(status="Completed")
        print(orders1)
        print(orders2)
        print(orders3)
        events = Event.objects.all().order_by("date_time")
        context = {
            'orders1' : orders1,
            'orders2' : orders2,
            'orders3' : orders3,
            'events' : events,
            'user' : user,
            'orders' : user.orders.all()
        }
        return render(request,'user_info.html',context)





    else:
        messages.error(request,'You do not have access to this page. Login to continue',extra_tags='no_access')
        return redirect('/')

def edit(request,user_id):
    if 'userID' in request.session:
        context = {
            'user' : User.objects.get(id=user_id)
        }
        return render(request,'user_edit.html',context)
    else:
        messages.error(request,'You do not have access to this page. Login to continue',extra_tags='no_access')
        return redirect('/')

def update(request,user_id):
    # if 'userID' in request.session:
    #     # Not Working: ('btjensen@mtu.edu',)
    #     errors = User.objects.update_validator(request.POST)

    #     if len(errors) > 0:
    #         for key, value in errors.items():
    #             messages.error(request,value,extra_tags=key)
    #         return redirect(f'/users/{user_id}/account')
    #     else:
    #         password_encoded = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    #         user = User.objects.get(id=user_id)
    #         user.first_name = request.POST['first_name'],
    #         user.last_name = request.POST['last_name'],
    #         user.email = request.POST['email'],
    #         user.password = password_encoded,
    #         user.phone_number = request.POST['phone_number']
    #         user.save()
    #         print('updated')
        return redirect(f'/users/{user_id}/account')
    else:
        messages.error(request,'You do not have access to this page. Login to continue',extra_tags='no_access')
        return redirect('/')

def destroy(request,user_id):
    if 'userID' in request.session:
        User.objects.get(id=user_id).delete()
        return redirect('/users')
    else:
        messages.error(request,'You do not have access to this page. Login to continue',extra_tags='no_access')
        return redirect('/')

def restaurant(request,restaurantID):
    if 'restaurantID' in request.session:
        restaurant = Restaurant.objects.filter(id=request.session['restaurantID'])
        if restaurant:
            return redirect('/restaurantlogin')
        else:
            request.session.flush()
            return redirect('/')
    elif 'userID' in request.session:
        user = User.objects.filter(id=request.session['userID'])
        restaurant = Restaurant.objects.filter(id=restaurantID)
        if user and restaurant:
            user = User.objects.get(id=request.session['userID'])
            restaurant = Restaurant.objects.get(id=restaurantID)
            check_events1 = restaurant.events.filter(status="In Progress")
            check_events2 = restaurant.events.filter(status="Completed")
            if check_events1:
                id1 = restaurant.events.filter(status="In Progress").order_by("date_time")[0].id
            else:
                id1 = -1
            if check_events2:
                id2 = restaurant.events.filter(status="Completed").order_by("-date_time")[0].id
            else:
                id2 = -1
            
            context = {
                'one_restaurant': restaurant,
                'id1': id1,
                'id2': id2,
                'one_menu': Menu.objects.filter(restaurant_id=restaurantID)
            }
            return render(request,'eventdetailuser.html',context)

        return redirect('/userlogin')
    return redirect('/')

def editroute(request):
    if 'userID' in request.session:
        user = User.objects.filter(id=request.session['userID'])
        if user:
            print('redirecting')
            return redirect(f"/users/{request.session['userID']}/account")
        else:
            request.session.flush()
            return redirect('/')
    elif 'restaurantID' in request.session:
        restaurant = Restaurant.objects.filter(id=request.session['restaurantID'])
        if restaurant:
            return redirect('/restaurantlogin/welcome')
        else:
            request.session.flush()
            return redirect('/')
    return render(request,'/')


    # if 'userID' in request.session:
    #     restaurant = Restaurant.objects.get(id=restaurantID)
    #     check_events1 = restaurant.events.filter(status="In Progress")
    #     check_events2 = restaurant.events.filter(status="Completed")
    #     if check_events1:
    #         id1 = restaurant.events.filter(status="In Progress").order_by("date_time")[0].id
    #     else:
    #         id1 = -1
    #     if check_events2:
    #         id2 = restaurant.events.filter(status="Completed").order_by("-date_time")[0].id
    #     else:
    #         id2 = -1

    #     print(restaurant.events.all())
    #     context = {
    #         'events' : Event.objects.filter(restaurant=restaurant).order_by("date_time"),
    #         'user' : request.session['userID'],
    #         'one_restaurant': restaurant,
    #         'id1': id1,
    #         'id2': id2,
    #     }
    #     return render(request,'user_restaurant.html',context)
    # else:
    #     messages.error(request,'You do not have access to this page. Login to continue',extra_tags='no_access')
    #     return redirect('/')