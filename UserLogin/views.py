from django.shortcuts import render, HttpResponse, redirect
from RestaurantEvent.models import Event
from .models import User, UserManager
from django.contrib import messages
import bcrypt

def index(request):
    # render homepage
    return render(request,'index.html')

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
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'], 
            # birthday = request.POST['bday'],
            email = request.POST['email'],
            password = password_encoded,
            phone_number = request.POST['phone_number']
        )
        # request.session['user_email'] = request.POST['email']
        # request.session['fname'] = request.POST['fname']

        return HttpResponse('Registered')


def login(request):
    errors = User.objects.login_validator(request.POST)
    print(errors)
    if len(errors) > 0:
        print('errors')
        for key, value in errors.items():
            messages.error(request,value,extra_tags=key)
        return redirect('/users')
    else:
        print('no errors')
    #     pass

        # user = User.objects.filter(email=request.POST['logemail'])
        # print(user)
        # if user:
        #     print("There's a user")
        #     if bcrypt.checkpw(request.POST['logpassword'].encode(), user[0].password.encode()):
        #         print("password")
        #         request.session['user_email'] = user[0].email
        #         request.session['fname'] = user[0].first_name
        #         request.session['user_id'] = user[0].id
        #         # return redirect('/success')
        #         user_id = user[0].id
        #         return redirect(f'/users/{user_id}')

        # else:
        #     print('Email/Password is incorrect or User does not exist')

    return HttpResponse('Did not work')

def users(request):
    return render(request,'user_login.html')
    
def user_info(request,user_id):
    context = {
        'events' : Event.objects.all()
    }
    return render(request,'user_welcome.html',context)
