from django.db import models

from product.models import Product, User

STATUS_CHOICES = (
    ('open', 'otkritit'),
    ('in_progress', 'v obrabotke'),
    ('canceled', 'otmenenni'),
    ('finished', 'zaversheni'),
)

class Order(models.Model):


    total_sum = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
                             on_delete=models.RESTRICT,
                             related_name='orders'),
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    products = models.ManyToManyField(Product,
                                      through='OrderItem')
    class Meta:
        db_table = 'order'

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.RESTRICT,
                              related_name='items')
    product = models.ForeignKey(Product,
                               on_delete= models.RESTRICT,
                               related_name='order_items')
    quantity = models.PositiveSmallIntegerField(default=1)
    class Meta:
        db_table = 'order_items'





