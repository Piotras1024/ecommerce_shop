from django.shortcuts import render
from django.shortcuts import get_object_or_404

from . models import Category, Product, ProductSize

from django.http import JsonResponse
from django.http import HttpResponse
# Create your views here.


def store(request):

    all_products = Product.objects.all()
    context = {'my_products': all_products}

    return render(request, 'store_clothes/store.html', context=context)


def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}


def list_category(request, category_slug=None):

    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    # context = {'category': category, 'products': products}

    return render(request, 'store_clothes/list-category.html', {'category':category, 'products':products})


def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    product_sizes = ProductSize.objects.filter(product=product).select_related('size')

    context = {
        'product': product,
        'product_sizes': product_sizes
    }

    return render(request, 'store_clothes/product-info.html', context=context)


