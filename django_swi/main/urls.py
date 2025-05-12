from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("item/create/", views.ItemCreateView.as_view(), name="item_create"),
    path("item/<int:pk>/update/", views.ItemUpdateView.as_view(), name="item_update"),
    path("item/<int:pk>/delete/", views.ItemDeleteView.as_view(), name="item_delete"),
    path("item/hello/", views.HelloWorldView.as_view(), name="hello_world"),
    path("item/random/", views.RandomView.as_view(), name="random_view"),
    path(
        "item/add-number/<int:num1>/<int:num2>/",
        views.AddNumbersView.as_view(),
        name="add_number",
    ),
]