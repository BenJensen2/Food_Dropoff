from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index), 
    path('<int:orderID>', views.orderDetail),
    path('<int:orderID>/cancel', views.orderDelete),
    path('<int:orderID>/confirm', views.orderConfirm),
    path('<int:orderID>/messsage', views.loadMessage),
    path('sendmsg', views.sendMessage),
    #catch route?
]