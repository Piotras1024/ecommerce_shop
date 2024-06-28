from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from store_clothes.models import Product, ProductSize, Size

import pprint


# Create your views here.


def cart_summary(request):
    cart = Cart(request)
    cart_items_with_sizes = {}

    for item in cart:
        product_sizes = ProductSize.objects.filter(product=item['product']).select_related('size')
        sizes_availability = {ps.size.size_name: ps.availability for ps in product_sizes}
        cart_items_with_sizes[item['product'].id] = {
            'item': item,
            'sizes_availability': sizes_availability
        }

    context = {
        'cart': cart,
        'cart_items_with_sizes': cart_items_with_sizes
    }

    # # Raise an exception with the pprint version of the dictionary
    # raise Exception(pprint.pformat(cart_items_with_sizes.items()))

    return render(request, 'cart/cart-summary.html', context=context)


def cart_add(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        size_name = request.POST.get('product_size')

        product = get_object_or_404(Product, id=product_id)
        size = get_object_or_404(Size, size_name=size_name)

        cart.add(product=product, product_qty=product_quantity, size=size)

        cart_quantity = cart.__len__()
        product_size_quantity = cart.cart[str(product_id)][str(size.id)]['qty']

        response = JsonResponse({'cart_qty': cart_quantity, 'product_size_qty': product_size_quantity})

        return response


def cart_delete(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = request.POST.get('product_id')
        size_id = request.POST.get('size_id')

        cart.delete(product_id=product_id, size_id=size_id)

        cart_quantity = cart.__len__()

        cart_total = cart.get_total()

        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})

        return response


def cart_update(request):


    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        size_name = request.POST.get('size_name')  # Pobieranie rozmiaru z formularza


        # Pobranie produktu na podstawie ID
        product = Product.objects.get(id=product_id)

        # pobranie rozmiaru na podstawie nazwy
        size = Size.objects.get(size_name=size_name)

        # Pobrać rozmiary powiązane z danym produktem
        product_sizes = ProductSize.objects.filter(product=product).select_related('size')

        # Tworzenie słownika dostępności dla rozmiarów powiązanych z produktem
        sizes_availability = {ps.size.size_name: ps.availability for ps in product_sizes}

        if product_quantity > sizes_availability.get(size_name, 0):
            return JsonResponse({
                'error': f'Produkt {product.title} jest dostępny tylko w ilości {sizes_availability[size_name]}'
            }, status=400)
        else:
            cart.update(product=product, product_qty=product_quantity, size=size)

        cart_quantity = cart.__len__()
        cart_total = cart.get_total()
        singe_total = cart.get_single_total(product_id)

        return JsonResponse({'qty': cart_quantity, 'total': cart_total, 'product_total': singe_total, 'sizes': sizes_availability})
