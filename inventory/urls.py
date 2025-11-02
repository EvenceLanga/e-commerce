from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Redirect root (/) → login page
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),

    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
   # inventory/urls.py
    path('logout/', views.logout_view, name='logout'),

    path('add_inventory_item/', views.add_inventory_item, name='add_inventory_item'),
    path('list/', views.inventory_list, name='inventory_list'),
    path('profile/', views.profile_view, name='profile'), 
    path("edit/<str:material>/", views.edit_inventory_item, name="inventory_edit"),
    path("delete/<str:material>/", views.delete_inventory_item, name="inventory_delete"),

    path('export/', views.export_inventory_excel, name='export_inventory_excel'),

]

