from decimal import Decimal
from itertools import product

from store_clothes.models import Product, ProductSize, Size


class Cart:

    def __init__(self, request):

        self.session = request.session

        # Returning user - obtain his/her existing session
        cart = self.session.get('session_key')

        # New user - generate new session

        if 'session_key' not in request.session:

            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, product_qty, size):

        product_id = str(product.id)
        size_id = str(size.id)

        if product_id not in self.cart:

            self.cart[product_id] = {}

        if size_id in self.cart[product_id]:
            self.cart[product_id][size_id]['qty'] = product_qty

        else:

            self.cart[product_id][size_id] = {'price': str(product.price), 'qty': product_qty, 'size': size.size_name}

        self.session.modified = True

    def delete(self, product_id,size_id ):

        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def update(self, product, product_qty, size):

        product_id = str(product.id)
        size_id = str(size.id)

        if product_id not in self.cart:

            self.cart[product_id] = {}

        if size_id in self.cart[product_id]:

            self.cart[product_id][size_id]['qty'] = product_qty

        else:

            self.cart[product_id][size_id] = {'price': str(product.price), 'qty': product_qty, 'size': size.size_name}

        self.session.modified = True

    def __len__(self):
        total_qty = 0
        for product_id, sizes in self.cart.items():
            for size_id, details in sizes.items():
                total_qty += details['qty']
        return total_qty

    def __iter__(self):
        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        cart_copy = self.cart.copy()

        for product in products:
            product_id = str(product.id)
            for size_id, details in cart_copy[product_id].items():
                try:
                    # Ensure size_id is a number before attempting to get the Size object
                    size_id_int = int(size_id)
                    size = Size.objects.get(id=size_id_int)
                except (ValueError, Size.DoesNotExist):
                    continue  # or handle the error appropriately
                item = {
                    'product': product,
                    'size': size,
                    **details,
                    'total': Decimal(details['price']) * details['qty']
                }
                yield item

    def get_total(self):
        total = Decimal('0.00')
        for item in self:
            total += item['total']
        return total

    def get_single_total(self, product_id):
        total = Decimal('0.00')
        product_id = str(product_id)
        if product_id in self.cart:
            for size_id, details in self.cart[product_id].items():
                total += Decimal(details['price']) * details['qty']
        return total
