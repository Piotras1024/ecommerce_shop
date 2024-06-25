from decimal import Decimal
from itertools import product

from store_clothes.models import Product, ProductSize


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

    def delete(self, product):

        product_id = str(product)

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

        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)

        # Przygotowanie nowego słownika do przechowywania informacji o produktach i rozmiarach
        cart_copy = {}

        for product in products:
            product_id = str(product.id)
            if product_id in self.cart:
                if isinstance(size_item, dict):  # Upewnij się, że size_item jest słownikiem
                    # Tworzenie wpisu dla każdego produktu, jeśli jeszcze nie istnieje
                    cart_copy[product_id] = cart_copy.get(product_id, {})
                    # Dodawanie informacji o każdym rozmiarze produktu
                    for size_id, details in self.cart[product_id].items():
                        # Dodawanie lub aktualizowanie informacji o rozmiarze
                        cart_copy[product_id][size_id] = {
                            **details,
                            'product': product,
                            'size': size_id  # Przechowujemy size_id dla wyraźności
                        }

        # Yieldowanie produktów z informacjami o rozmiarze
        for product_items in cart_copy.values():
            for size_item in product_items.values():
                yield size_item

    def get_total(self):
        for size_item in self:
            return size_item['price'] + size_item['qty']

    def get_total_single(self, product):
        product_id = str(product.id)
        for size_item in self[product_id]:
            return size_item['price'] + size_item['qty']
