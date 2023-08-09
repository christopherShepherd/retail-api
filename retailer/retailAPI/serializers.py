from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User
from . import models


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart 
        fields = ['item', 'quantity', 'unit_price', 'price']
        read_only_fields = ['unit_price', 'price']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'title']


# add validation to title, price
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ['id', 'title', 'price', 'featured', 'category']

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer(read_only=True)
        return super().to_representation(instance)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = ['item', 'quantity', 'unit_price', 'price']
        validators = [UniqueTogetherValidator(queryset=models.Item.objects.all(),
                                              fields=['order', 'item'])]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = ['id', 'user', 'items', 'total', 'status', 'date', 'delivery_crew']
        read_only_fields = ['id', 'user', 'items', 'total', 'date']


# necessary to add validation
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
