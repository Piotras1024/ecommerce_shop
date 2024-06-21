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
    sizes_availability = [(ps.size.size_name, ps.availability) for ps in product_sizes]

    # Dodajemy informację, czy są dostępne jakiekolwiek rozmiary
    any_available = any(availability > 0 for _, availability in sizes_availability)

    context = {
        'product': product,
        'sizes_availability': sizes_availability,
        'any_available': any_available
    }

    return render(request, 'store_clothes/product-info.html', context=context)

