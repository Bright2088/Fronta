from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify



class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# Product Model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
            ordering = ['-created']
            indexes = [
                models.Index(fields=['slug']),
                models.Index(fields=['name']),
            ]

    def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.name)
            super().save(*args, **kwargs)

    def __str__(self):
            return self.name


# Customer Profile (Optional, extending User)
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"Cart {self.id} ({self.user.username})"
    
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


# Cart Item
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def total_price(self):
        return self.quantity * self.product.price


# Order (After Checkout)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} ({self.user.username})"

    def calculate_total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)



# Order Item
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at the time of purchase

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Deleted Product'}"
