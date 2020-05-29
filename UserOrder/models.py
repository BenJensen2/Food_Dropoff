from django.db import models
from UserLogin.models import User
from RestaurantItem.models import Item
from RestaurantEvent.models import Event
from RestaurantMenu.models import Menu

class OrderQuantityManager(models.Manager):
    def validator(self, postData):
        errors = {}
        #Make sure quantities are numbers and non negative
        print(postData)
        for item_id, quantity in postData.items():
            if item_id != "csrfmiddlewaretoken":
                if not quantity.isdigit():
                    errors["quantity"] = "Make sure all item quantities are positive integers"
        return errors

class Order(models.Model):
    user =  models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="orders", on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderQuantity(models.Model):
    item =  models.ForeignKey(Item, related_name="quantities", on_delete=models.CASCADE)
    order =  models.ForeignKey(Order, related_name="quantities", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderQuantityManager()
