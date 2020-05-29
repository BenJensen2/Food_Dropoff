from django.shortcuts import render, HttpResponse, redirect
from RestaurantEvent.models import Event
from .models import User, UserManager
from django.contrib import messages
import bcrypt

def index(request):
    # render homepage
    return render(request,'homepage.html')

def users(request):
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
        context = {
            'events' : Event.objects.all().order_by("date_time"),
            'user' : User.objects.get(id=user_id)
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
    if 'userID' in request.session:
    # Not Working: ('btjensen@mtu.edu',)
    # errors = User.objects.update_validator(request.POST)

    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request,value,extra_tags=key)
    #     return redirect(f'/users/{user_id}/account')
    # else:
    #     password_encoded = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    #     user = User.objects.get(id=user_id)
    #     user.first_name = request.POST['first_name'],
    #     user.last_name = request.POST['last_name'],
    #     user.email = request.POST['email'],
    #     user.password = password_encoded,
    #     user.phone_number = request.POST['phone_number']
    #     user.save()
    #     print('updated')
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