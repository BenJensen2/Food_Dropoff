from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def registration_validator(self,postData):
        errors = {}
        not_blank = "This field cannot be left blank."
        fewer_2 = "This field cannot be fewer than 2 characters in length."
        longer_3 = "This field cannot be longer than 30 characters in length."
        invalid_email = "Invalid email address."
        
        # First Name Validations
        if len(postData['first_name']) == 0:
            errors['first_name'] = not_blank
        elif len(postData['first_name']) < 2:
            errors['first_name'] = fewer_2
        elif len(postData['first_name']) > 30:
            errors['first_name'] = longer_3

        # Last Name Validations
        if len(postData['last_name']) == 0:
            errors['last_name'] = not_blank
        elif len(postData['last_name']) < 2:
            errors['last_name'] = fewer_2
        elif len(postData['last_name']) > 30:
            errors['last_name'] = longer_3

        # Include Birthday Validations

        # Email Validations
        EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
        user = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = not_blank
        elif len(postData['email']) < 6:
            errors['email'] = invalid_email
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = invalid_email
        elif user:
            errors['email'] = "Please use another email address."

        # Password Validations
        PASS_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$")
        if len(postData['password']) == 0:
            errors['password'] = not_blank
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long."
        elif not PASS_REGEX.match(postData['password']):
            errors['password'] = "Password must contain 1 uppercase, 1 lowercase, 1 number, and 1 special character."
        elif postData['password'] != postData['confirmpw']:
            errors['password'] = "Passwords do not match."

        return errors

    def login_validator(self,postData):
        errors = {}
        user_pass = 'Email/Password is incorrect or User does not exist'
        user = User.objects.filter(email=postData['logemail'])
        try:
            # user[1]
            if not bcrypt.checkpw(postData['logpassword'].encode(), user[0].password.encode()):
                print('wrong password')
                errors['login'] = user_pass
        except: 
            errors['login'] = user_pass

        return errors
# Have Not Tested
    # def update_validator(self,postData):
        
    #     errors = {}
    #     not_blank = "This field cannot be left blank."
    #     fewer_2 = "This field cannot be fewer than 2 characters in length."
    #     longer_3 = "This field cannot be longer than 30 characters in length."
    #     invalid_email = "Invalid email address."
        
    #     # First Name Validations
    #     if len(postData['fname']) == 0:
    #         errors['fname'] = not_blank
    #     elif len(postData['fname']) < 2:
    #         errors['fname'] = fewer_2
    #     elif len(postData['fname']) > 30:
    #         errors['fname'] = longer_3

    #     # Last Name Validations
    #     if len(postData['lname']) == 0:
    #         errors['lname'] = not_blank
    #     elif len(postData['lname']) < 2:
    #         errors['lname'] = fewer_2
    #     elif len(postData['lname']) > 30:
    #         errors['lname'] = longer_3


    #     # Email Validations
    #     EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
    #     user = User.objects.filter(email_address=postData['email'])
    #     if len(postData['email']) == 0:
    #         errors['email'] = not_blank
    #     elif len(postData['email']) < 6:
    #         errors['email'] = invalid_email
    #     elif not EMAIL_REGEX.match(postData['email']):
    #         errors['email'] = invalid_email
    #     elif user:
    #         errors['email'] = "Please use another email address."

    #     return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()