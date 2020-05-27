from django.urls import path #Include path function
from . import views # import views file within the same folder (from .)

# RESTful
urlpatterns = [
    path('',views.index),
    path('users',views.users),
    path('users/register',views.register),
    path('users/create',views.create),
    path('users/login',views.login),
    # path('user_login/new', views.new),
    # path('user_login/new/create',views.create),
    path('users/<int:user_id>', views.user_info),
    # path('user_login/<int:show_id>/edit', views.edit),
    # path('user_login/<int:show_id>/edit/update', views.update),
    # path('user_login/<int:show_id>/destroy', views.destroy),
]