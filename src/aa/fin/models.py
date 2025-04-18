from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255)
    monthly_budget = models.DecimalField(decimal_places=2, max_digits=10)
    daily_budget = models.DecimalField(decimal_places=2, max_digits=10)
    dayparting = models.JSONField(default=list)


class Spend(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    datetime = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
