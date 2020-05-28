from django.db import models
from RestaurantLogin.models import Restaurant, RestaurantManager

class Item(models.Model):
    item_title = models.CharField(max_length=255)
    item_description = models.TextField()
    item_price = models.DecimalField(max_digits = 10, decimal_places=2)
    # menus
    restaurant = models.ForeignKey(Restaurant,related_name="items", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)