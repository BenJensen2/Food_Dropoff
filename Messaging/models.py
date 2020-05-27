from django.db import models
from UserOrder.models import Order

class Message(models.Model):
    order =  models.ForeignKey(Order, related_name="messages", on_delete=models.CASCADE)
    sent_by = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    