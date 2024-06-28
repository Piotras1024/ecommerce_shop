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

    def delete(self, productsize_id):

        if productsize_id in self.cart:
            del self.cart[productsize_id]

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

