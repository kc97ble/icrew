from django.db import models
from django.contrib.auth.models import User


class Drink(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return "D{} - {}".format(self.id, self.title)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "R{} - {} - {} - {}".format(
            self.id, self.user.username, self.drink.title, self.note
        )
