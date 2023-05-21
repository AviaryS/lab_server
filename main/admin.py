from django.contrib import admin

from main.models import User, Product, Order, Cart

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)