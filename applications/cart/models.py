from django.db import models

# Create your models here.
from applications.board.models import Post, User


class Cart(models.Model): # корзина
    CART_STATUS = (
        ('IN_PROCESSING', 'in_processing'),
        ('COMPLETED', 'completed'), # ЗАВЕРШЕННЫЙ
        ('DECLINED', 'declined') # ОТКЛОНЕННЫЙ
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    status = models.CharField(max_length=30, choices=CART_STATUS, default='in_processing')

    def str(self):
        return self.user.email


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='cart_item')
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def str(self):
        return f'{self.post} in {self.cart} cart'

    def save(self, *args, **kwargs):
        self.total_cost = self.post.price * self.quantity
        super(CartItem, self).save(*args, **kwargs)
