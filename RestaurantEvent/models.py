from django.db import models
from Location.models import Location
from RestaurantLogin.models import Restaurant, RestaurantManager
from RestaurantMenu.models import Menu
import datetime
import re

class EventManager(models.Manager):
    def validator(self, postData):
        errors = {}
        #Address field
        if not "address" in postData:
            errors["address"] = "Address must be included"
        elif len(postData["address"]) < 1:
            errors["address"] = "Address must be included"
        #City field
        if not "city" in postData:
            errors["city"] = "City must be included"
        elif len(postData["city"]) < 1:
            errors["city"] = "City must be included"
        #State field
        if not "state" in postData:
            errors["state"] = "State must be included"
        elif len(postData["state"]) < 1:
            errors["state"] = "State must be included"
        #Zip Code field
        #Make sure zip code is 5 digits
        if not "zip_code" in postData:
            errors["zip_code"] = "Zip Code must be included"
        else:
            zipRegex = re.compile(r'[0-9]{5}')
            if not zipRegex.match(postData["zip_code"]):
                errors["zip_code"] = "Please enter a 5 digit zip code"
            if len(postData["zip_code"]) < 1:
                errors["zip_code"] = "Zip Code must be included"
        #Date Time Field
        if not "date" in postData:
            errors["date"] = "Please specify a date"
        else:
            if len(postData["date"]) < 1:
                errors["date"] = "Please specify a date"
            #Make sure date is in the future
            elif datetime.datetime.strptime(postData["date"], "%Y-%m-%dT%H:%M") < datetime.datetime.now():
                errors["date"] = "Event must be in the future"
        #Minimum orders
        if not "min_orders" in postData:
            errors["min_orders"] = "Please specify a minimum number of orders"
        elif int(postData["min_orders"]) < 0:
            errors["min_orders"] = "Minimum orders limit must be positive"
        #Maximum orders
        if not "max_orders" in postData:
            errors["max_orders"] = "Please specify a maximum number of orders"
        elif int(postData["max_orders"]) < 0:
            errors["max_orders"] = "Maximum order limit must be greater than 0"
        #Minimum amount per order
        if not "min_per_order" in postData:
            errors["min_per_order"] = "Please specify a minimum per order cost"
        elif int(postData["min_per_order"]) < 0:
            errors["min_per_order"] = "Minimum per order cost must be greater than 0"
        #Make sure the menu has items
        return errors

class Event(models.Model):
    restaurant =  models.ForeignKey(Restaurant, related_name="events", on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu,related_name="events",on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    date_time = models.DateTimeField()
    notes = models.TextField()
    location = models.ForeignKey(Location, related_name="events", on_delete=models.CASCADE)
    minimum_orders = models.IntegerField()
    maximum_orders = models.IntegerField()
    minimum_amount_per_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()
