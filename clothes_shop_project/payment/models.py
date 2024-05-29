from django.db import models

from django.contrib.auth.models import User

from store_clothes.models import Product


class ShippingAddress(models.Model):

    full_name = models.CharField(max_length=300)

    email = models.EmailField(max_length=255)

    address1 = models.CharField(max_length=300)

    address2 = models.CharField(max_length=300)

    city = models.CharField(max_length=255)


    # Optional

    state = models.CharField(max_length=255, null=True, blank=True)

    zipcode = models.CharField(max_length=255, null=True, blank=True)


    # FK

    # Authenticated / not authenticated users (bear in mind)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:

        verbose_name_plural = 'Shipping Address'

    def __str__(self):

        return 'Shipping Address ' + str(self.id) + ' -> ' + self.full_name


class Order(models.Model):

    full_name = models.CharField(max_length=300)

    email = models.EmailField(max_length=300)

    shipping_address = models.TextField(max_length=1500)

    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    date_order = models.DateTimeField(auto_now_add=True)

    # Foreign Key

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):

        return 'Order - #' + str(self.id) + ' -> ' + self.full_name


class OrderItem(models.Model):


    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    # FK

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)


    def __str__(self):

        return 'Order Item - #' + str(self.id)
