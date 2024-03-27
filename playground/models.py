from django import forms
from django.db import models
from django.contrib.auth.models import User

from storefront import settings

class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name
      
class Product(models.Model):
    CATEGORY = (
        ('Women fashion', 'Women fashion'),
        ('Shoes', 'Shoes'),
        ('Home appliances', 'Home appliances'),
        ('Electronics', 'Electronics'),
        ('Furniture', 'Furniture'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField('Product', related_name='carts', blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart for {self.user.username}"

class Order(models.Model):
	STATUS = (
			('pending', 'Pending'),
			('delivery', 'Out for delivery'),
			('delivered', 'Delivered'),
			)

	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	total_price = models.DecimalField(max_digits=10, decimal_places=2)
	payment_status = models.CharField(max_length=20, default='Pending')
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	# def __str__(self):
	# 	return self.product.name

class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_lines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    products = models.ManyToManyField(Product)
    # You might have other fields in your Payment model

    def __str__(self):
        if self.user:
            return f"Payment for {self.user.username}"
        else:
            return "Payment without user"


	
