from django.db import models
from versatileimagefield.fields import VersatileImageField
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    # username = models.CharField(max_length=255, unique=True)
    # groups = models.ManyToManyField(Group, related_name='marketplace_user_set')
    # user_permissions = models.ManyToManyField(Permission, related_name='marketplace_user_permissions_set')
    telegram_id = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, blank=True)
    is_seller = models.BooleanField(default=False)  # To differentiate between buyers and sellers
    is_active = models.BooleanField(default=True)  
    def __str__(self):
        return self.username

class Textbook(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    school_class = models.CharField(max_length=50) 
    publisher = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="textbooks")
    description = models.TextField(blank=True)
    whatsapp_contact = models.CharField(max_length=100, blank=True, null=True)
    viber_contact = models.CharField(max_length=100, blank=True, null=True)
    telegram_contact = models.CharField(max_length=100, blank=True, null=True)
    phone_contact = models.CharField(max_length=100, blank=True, null=True)
    condition = models.CharField(max_length=50, choices=[
        ('New', 'New'),
        ('Used - Excellent', 'Used - Excellent'),
        ('Used - Good', 'Used - Good'),
        ('Used - Fair', 'Used - Fair'),
    ], default='Used - Good')
    image = VersatileImageField(upload_to='textbook_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title

class Order(models.Model):
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    