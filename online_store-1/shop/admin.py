from django.contrib import admin
from .models import Category, SubCategory, Brand, Product, Review, CartItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'subcategory', 'brand', 'price', 'rating')
    list_filter = ('category', 'subcategory', 'brand')
    search_fields = ('name', 'description', 'details')
    readonly_fields = ('rating',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'surname', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'surname', 'text')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'session_key', 'quantity')
    search_fields = ('session_key', 'product__name')
