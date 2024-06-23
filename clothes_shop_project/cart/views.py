from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from store_clothes.models import Product, ProductSize


# Create your views here.


def cart_summary(request):

    cart = Cart(request)

    return render(request, 'cart/cart-summary.html', {'cart': cart})


def cart_add(request):

    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, product_qty=product_quantity)

        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity})

        return response


def cart_delete(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

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
        # Pobrać rozmiary powiązane z danym produktem
        product_sizes = ProductSize.objects.filter(product=product).select_related('size')
        # Tworzenie słownika dostępności dla rozmiarów powiązanych z produktem
        sizes_availability = {ps.size.size_name: ps.availability for ps in product_sizes}

        if product_quantity > sizes_availability.get(size_name, 0):
            return JsonResponse({
                'error': f'Produkt {product.title} jest dostępny tylko w ilości {sizes_availability[size_name]}'
            }, status=400)
        else:
            cart.update(product=product_id, qty=product_quantity)

        cart_quantity = cart.__len__()
        cart_total = cart.get_total()

        return JsonResponse({'qty': cart_quantity, 'total': cart_total, 'sizes': sizes_availability})
