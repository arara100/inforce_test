from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date


class Employee(AbstractUser):
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    items = models.TextField()

    class Meta:
        unique_together = ('restaurant', 'date')

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"


class Vote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    class Meta:
        unique_together = ('employee', 'date')
