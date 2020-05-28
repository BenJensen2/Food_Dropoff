from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index), 
    path('<int:orderID>', views.orderDetail),
    path('<int:orderID>/cancel', views.orderDelete),
    path('<int:orderID>/confirm', views.orderConfirm),
    path('<int:orderID>/message', views.loadMessage),
    path('<int:orderID>/refresh', views.refreshMessage),
    path('sendmsg', views.sendMessage),
    #catch route?
]