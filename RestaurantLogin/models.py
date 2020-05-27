from django.db import models
from Location.models import Location
import re
import bcrypt

class RestaurantManager(models.Manager):
    def reg_validator(self, postData):
        errors={}
        if len(postData['restaurant_name']) < 2:
            errors['restaurant_name'] = "Restaurant name must be at least 2 characters in length"
        
        if len(postData['cuisine']) < 4:
            errors['cuisine'] = "Cuisine must be at least 4 characters in length"

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters in length"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters in length"

        if len(postData['address']) < 5:
            errors['address'] = "Street address must be at least 5 characters in length"

        if len(postData['city']) < 3:
            errors['city'] = "City must be at least 3 characters in length"

        if len(postData['state']) != 2:
            errors['state'] = "Choose state from the dropdown"

        if len(postData['zip_code']) != 5:
            errors['zip_code'] = "Enter a 5-digit zip code"
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter a valid email address"
        elif len(Restaurant.objects.filter(email_address__iexact=postData['email'])) > 0:
            errors['email'] = "An account already exists for this email"

        if len(postData['phone_number']) != 10:
            errors['phone_number'] = "Enter a valid phone number with area code without dashes, parentheses or spaces"
        

        PW_REGEX = re.compile(r'^(?=.*\d)[a-zA-Z\d]{8,20}$')
        if not PW_REGEX.match(postData['password']):
            errors['password'] = "Password must be between 8-20 characters in length and must contain at least one number"
        
        if not postData['password'] == postData['confirmpw']:
            errors['confirmpw'] = "Passwords do not match - please confirm password again"

        return errors      

    def pw_validator(self, postData):
        errors={}
        restaurant = Restaurant.objects.filter(email_address=postData['logemail'])
        if restaurant:
            logged_user = restaurant[0]
            if bcrypt.checkpw(postData['logpassword'].encode(), logged_user.password.encode()) == False:
                errors = {'login_failed': 'Incorrect email or password'}
        else:
            errors = {'login_failed': 'Incorrect email or password'}

        return errors

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cuisine = models.CharField(max_length=50)
    location = models.ForeignKey(Location, related_name="restaurants", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    email_address = models.CharField(max_length=50)
    password = models.CharField(max_length = 70)
    # events: All events assocated with this restaurant
    # menus: All menus assocated with this restaurant
    # items: All items assocated with this restaurant

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RestaurantManager()


#    class RestaurantManager(models.Manager):
#     def register_validator(self,postData):
#         errors = {}
#         not_blank = "This field cannot be left blank."
#         fewer_2 = "This field cannot be fewer than 2 characters in length."
#         longer_3 = "This field cannot be longer than 30 characters in length."
#         invalid_email = "Invalid email address."
        
#         # # Name Validations
#         # if len(postData['name']) == 0:
#         #     errors['name'] = not_blank
#         # elif len(postData['name']) < 2:
#         #     errors['name'] = fewer_2
#         # elif len(postData['name']) > 30:
#         #     errors['name'] = longer_3

#         # # Owner Name Validations
#         # if len(postData['owner']) == 0:
#         #     errors['owner'] = not_blank
#         # elif len(postData['owner']) < 2:
#         #     errors['owner'] = fewer_2
#         # elif len(postData['owner']) > 30:
#         #     errors['owner'] = longer_3

#         # # Address Validations
#         # if len(postData['address']) == 0:
#         #     errors['address'] = not_blank
#         # elif len(postData['address']) < 2:
#         #     errors['address'] = fewer_2
#         # elif len(postData['address']) > 100:
#         #     errors['address'] = longer_3


#         # Include Birthday Validations

#         # Email Validations
#         EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
#         user = User.objects.filter(email_address=postData['email'])
#         if len(postData['email']) == 0:
#             errors['email'] = not_blank
#         elif len(postData['email']) < 6:
#             errors['email'] = invalid_email
#         elif not EMAIL_REGEX.match(postData['email']):
#             errors['email'] = invalid_email
#         elif user:
#             errors['email'] = "Please use another email address."

#         # Password Registration Validations
#         PASS_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$")
#         if len(postData['pword']) == 0:
#             errors['pword'] = not_blank
#         elif len(postData['pword_confirm']) == 0:
#             errors['pword_confirm'] = not_blank
#         elif len(postData['pword']) < 8:
#             errors['pword'] = "Password must be at least 8 characters long."
#         elif not PASS_REGEX.match(postData['pword']):
#             errors['pword'] = "Password must contain 1 uppercase, 1 lowercase, 1 number, and 1 special character."
#         elif postData['pword'] != postData['pword_confirm']:
#             errors['pword_confirm'] = "Passwords do not match."
        
#         return errors

#     def login_validator(self,postData):
#         errors = {}
#         user_pass = 'Email/Password is incorrect or User does not exist'
#         user = User.objects.filter(email_address=postData['email'])
#         if not user:
#             errors['login'] = user_pass
#         elif not bcrypt.checkpw(postData['login_pword'].encode(), user[0].password.encode()):
#             errors['login'] = user_pass

#         return errors

#     def update_validator(self,postData):
        
#         errors = {}
#         not_blank = "This field cannot be left blank."
#         fewer_2 = "This field cannot be fewer than 2 characters in length."
#         longer_3 = "This field cannot be longer than 30 characters in length."
#         invalid_email = "Invalid email address."
        
#         # # First Name Validations
#         # if len(postData['name']) == 0:
#         #     errors['name'] = not_blank
#         # elif len(postData['name']) < 2:
#         #     errors['name'] = fewer_2
#         # elif len(postData['name']) > 30:
#         #     errors['name'] = longer_3

#         # # Owner Name Validations
#         # if len(postData['owner']) == 0:
#         #     errors['owner'] = not_blank
#         # elif len(postData['owner']) < 2:
#         #     errors['owner'] = fewer_2
#         # elif len(postData['owner']) > 30:
#         #     errors['owner'] = longer_3

#         # # Address Validations
#         # if len(postData['address']) == 0:
#         #     errors['address'] = not_blank
#         # elif len(postData['address']) < 2:
#         #     errors['address'] = fewer_2
#         # elif len(postData['address']) > 100:
#         #     errors['address'] = longer_3

#         # Email Validations
#         EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
#         user = User.objects.filter(email_address=postData['email'])
#         if len(postData['email']) == 0:
#             errors['email'] = not_blank
#         elif len(postData['email']) < 6:
#             errors['email'] = invalid_email
#         elif not EMAIL_REGEX.match(postData['email']):
#             errors['email'] = invalid_email
#         elif user:
#             errors['email'] = "Please use another email address."

#         return errors