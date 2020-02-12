from django.urls import path
from .views import OrderAddView, OrderListView, OrderHomeView

urlpatterns = [
    path("", OrderHomeView.as_view(), name="orders-home"),
    path("add/", OrderAddView.as_view(), name="orders-add"),
    path("list/", OrderListView.as_view(), name="orders-list"),
]
