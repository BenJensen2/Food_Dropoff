from django.urls import path #Include path function
from . import views # import views file within the same folder (from .)

# RESTful
# Starts with menu/
urlpatterns = [
    path('',views.index),
    path('new', views.newMenu),
    path('new/create',views.create),
    path('new/addItem', views.addItem),
    path('new/<int:itemID>/removeItem', views.removeItem),

    path('checkRID/<int:restaurantID>', views.validateRID),

    path('<int:menuID>/content', views.menuContent)

    # path('restaurant_menu/<int:show_id>', views.show_info),
    # path('restaurant_menu/<int:show_id>/edit', views.edit),
    # path('restaurant_menu/<int:show_id>/edit/update', views.update),
    # path('restaurant_menu/<int:show_id>/destroy', views.destroy),
]