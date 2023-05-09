from datetime import timedelta

from django.contrib.auth.models import User
from django.utils.datetime_safe import date
from rest_framework import serializers

from store.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = 'name', 'quantity', 'is_active'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'username', 'email', 'first_name', 'last_name'


