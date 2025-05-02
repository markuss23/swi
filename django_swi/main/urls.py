from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('item/create/', views.ItemCreateView.as_view(), name='item_create'),
]