from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

import logging

from .cart import Cart
from store_clothes.models import Product, ProductSize, Size


logger = logging.getLogger('custom_logger')

# Create your views here.


def cart_summary(request):

    cart = Cart(request)
    logger.info(f'cart_summary: {{cart}}')

    context = {'cart': cart}

    return render(request, 'cart/cart-summary.html', context=context)


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':

        try:
            productsize_id = request.POST.get('productsize_id')
        except None:
            pass


        product_quantity = int(request.POST.get('product_quantity'))

        # raise Exception(productsize_id, product_quantity)

        cart.add(productsize_id=productsize_id, product_qty=product_quantity)

        cart_quantity = cart.__len__()

        response = JsonResponse({'productsize_id': productsize_id, 'product_quantity': product_quantity})

        return response


def cart_delete(request):

    cart = Cart(request)
    logger.info(f'productsize_id: {request.POST.get("productsize_id")}')
    if request.POST.get('action') == 'post':

        productsize_id = request.POST.get('productsize_id')


        cart.delete(productsize_id)

        cart_quantity = cart.__len__()

        cart_total = cart.get_total()

        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})

        return response


def cart_update(request):


    cart = Cart(request)

    if request.POST.get('action') == 'post':
        productsize_id = request.POST.get('productsize_id')

        product_qty = int(request.POST.get('product_qty'))

        cart.update(productsize_id, product_qty)

        cart_quantity = cart.__len__()
        cart_total = cart.get_total()
        single_total = cart.get_single_total(int(productsize_id))


        return JsonResponse({'qty': cart_quantity, 'total': cart_total, 'product_total': single_total })
