from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils.datetime_safe import date


class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def is_not_deactivatable(self):
        two_month_before = (date.today() - timedelta(days=60))
        return self.pk is None or self.created_at.date() > two_month_before

    def save(self, *args, **kwargs):
        if self.is_not_deactivatable() and self.is_active is False:
            raise Exception("You cannot deactivate a product within first 2 months")
        super(Product, self).save(*args, **kwargs)
