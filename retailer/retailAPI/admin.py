from django.contrib import admin
from .models import Item, Category, Order

admin.site.register([Item, Category, Order])
