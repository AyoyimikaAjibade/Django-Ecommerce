from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=254, unique=True)
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=254, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=2457, default='')
    media = models.ImageField()
    price = models.DecimalField(max_digits=9, decimal_places=2)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail',  args=[str(self.id)])

    def get_add_to_cart_url(self):
        return reverse('orders:add_to_cart', args=[str(self.id)])

    def get_remove_from_cart_url(self):
        return reverse('orders:remove_from_cart', args=[str(self.id)])

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.user.username
