from django.contrib import admin
from django import forms
from .models import Category, Product, Size, ProductSize


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size_name']
    search_fields = ['size_name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']
    search_fields = ['name']
    filter_horizontal = ['sizes']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'category', 'brand', 'price']
    list_filter = ['category', 'brand']
    search_fields = ['title', 'brand', 'category__name']


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'availability']
    list_filter = ['product', 'size']
    search_fields = ['product__title', 'size__size_name']
