from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):

    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    sizes = models.ManyToManyField('Size', related_name='categories')

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])


class Size(models.Model):
    size_name = models.CharField(max_length=6, unique=True)

    class Meta:
        verbose_name_plural = "sizes"

    def __str__(self):
        return self.size_name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default='un-branded')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/')

    class Meta:
        verbose_name_plural = "products"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-info', args=[self.slug])

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            self.create_sizes()

    def create_sizes(self):
        # This function is now called only once when the product is created.
        for size in self.category.sizes.all():
            ProductSize.objects.get_or_create(product=self, size=size)


class ProductSize(models.Model):
    product = models.ForeignKey(Product, related_name='product_sizes', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, related_name='product_sizes', on_delete=models.CASCADE)
    availability = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('product', 'size'),)

    def __str__(self):
        return f"{self.product.title} - {self.size.size_name}"


# Signal to handle post-save product creation for existing products
@receiver(post_save, sender=Product)
def create_product_sizes(instance, created, **_):
    if created:
        instance.create_sizes()
