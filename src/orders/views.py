from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Order, Drink


class OrderAddView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(
            request, "orders/order_add/get.html", {"drinks": Drink.objects.all()}
        )

    def post(self, request, *args, **kwargs):
        if len(request.POST["drink"]) != 1:
            return HttpResponseBadRequest()
        if Order.objects.filter(user=request.user).exists():
            return HttpResponse("You cannot order twice. Do you think you can hack my system?")
        drink = Drink.objects.get(id=request.POST["drink"][0])
        note = request.POST["note"]
        order = Order.objects.create(user=request.user, drink=drink, note=note)
        return HttpResponse(
            "Added: {} - {} - {}".format(
                order.user.username, order.drink.title, order.note
            )
        )


class OrderListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(
            request, "orders/order_list.html", {"orders": Order.objects.all()}
        )


class OrderHomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user).first()
        return render(request, "orders/order_home.html", {"order": order})

    def post(self, request, *args, **kwargs):
        if request.POST["action"] == "remove-order":
            Order.objects.filter(user=request.user).delete()
            return HttpResponse("Order removed")
        else:
            return HttpResponseBadRequest()
