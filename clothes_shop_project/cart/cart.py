from decimal import Decimal
from itertools import product
import logging

from store_clothes.models import Product, ProductSize, Size

logger = logging.getLogger('custom_logger')


class Cart:

    def __init__(self, request):

        self.session = request.session

        # Returning user - obtain his/her existing session
        cart = self.session.get('cart')

        # New user - generate new session

        if 'cart' not in request.session:

            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, productsize_id, product_qty):

        self.cart[productsize_id] = product_qty

        self.session.modified = True

        logger.info(f'Added product {self.cart}')


    def delete(self, product_id, size_id):

        if product_id in self.cart:
            if size_id in self.cart[product_id]:
                del self.cart[product_id][size_id]

                # Jeśli po usunięciu rozmiaru, produkt nie ma więcej rozmiarów w koszyku, usuń również produkt
                if not self.cart[product_id]:
                    del self.cart[product_id]

        self.session.modified = True

    def update(self, productsize_id, product_qty):

        self.cart[productsize_id] = product_qty

        self.session.modified = True

        logger.info(f'Updated {self.cart}')


    def __len__(self):
        total_qty = 0
        for qty in self.cart.values():
                total_qty += qty
        return total_qty

    def __iter__(self):
        for product_size_id, qty in self.cart.items():
            product_size_object = ProductSize.objects.filter(id=product_size_id)[0]
            result = {
                'product_size_object': product_size_object,
                'qty': qty,
                'qtys': list(range(1, product_size_object.availability + 1))
            }
            logger.info(f'product_item: {result}')
            yield result






    # def __iter__(self):
    #     all_product_ids = self.cart.keys()
    #     products = Product.objects.filter(id__in=all_product_ids)
    #     cart_copy = self.cart.copy()
    #
    #     for product in products:
    #         product_id = str(product.id)
    #         for size_id, details in cart_copy[product_id].items():
    #             try:
    #                 # Ensure size_id is a number before attempting to get the Size object
    #                 size_id_int = int(size_id)
    #                 size = Size.objects.get(id=size_id_int)
    #             except (ValueError, Size.DoesNotExist):
    #                 continue  # or handle the error appropriately
    #             item = {
    #                 'product': product,
    #                 'size': size,
    #                 **details,
    #                 'total': Decimal(details['price']) * details['qty']
    #             }
    #             yield item

    def get_total(self):
        total = Decimal('0.00')
        for item in self:
            total += item["product_size_object"].product.price * item['qty']

        return total

    def get_single_total(self, product_size_id):

        for item in self:
            logger.info(f'id = {item["product_size_object"].id}')
            if item["product_size_object"].id == product_size_id:
                return item["product_size_object"].product.price * item['qty']

