from django.db import models
from RestaurantLogin.models import Restaurant, RestaurantManager
from RestaurantItem.models import Item

class Menu(models.Model):
    name = models.CharField(max_length=100)
    # events_included 
    restaurant = models.ForeignKey(Restaurant,related_name="menus", on_delete=models.CASCADE)
    items = models.ManyToManyField(Item,related_name="menus")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)