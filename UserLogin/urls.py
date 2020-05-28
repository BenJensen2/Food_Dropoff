from django.urls import path #Include path function
from . import views # import views file within the same folder (from .)

# RESTful
# Project URL: localhost:8000/
urlpatterns = [
    path('',views.index),                               # Home Page
    path('users',views.users),                          # Login Page
    path('users/login',views.login),                    # Login Function
    path('users/logout',views.logout),                  # Logout Function
    path('users/register',views.register),              # Register Page
    path('users/create',views.create),                  # Create User Function
    path('users/<int:user_id>', views.user_info),       # User Info Page
    path('users/<int:user_id>/account', views.edit),    # Edit Account Page
    path('users/<int:user_id>/update',views.update),    # Update Account Function: Not Working
    path('users/<int:user_id>/destroy',views.destroy),  # Delete User Function
]