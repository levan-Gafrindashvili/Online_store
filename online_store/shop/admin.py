from django.contrib import admin
from .models import Category, SubCategory, Brand, Product, Review, CartItem

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(CartItem)
