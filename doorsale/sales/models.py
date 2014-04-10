from django.db import models
from django.conf import settings

from doorsale.catalog.models import Product
from doorsale.finance.models import TaxCategory 


class Cart(models.Model):
    """
    Represents customer's shopping basket
    """
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)  
    
    def sub_total(self):
        """
        Sub total of cart items
        """
        sub_total = 0.0
        for item in self.items:
            sub_total += item.sub_total()
        
        return sub_total
    
    def get_taxes(self):
        """
        Total taxes applied on cart items
        """
        taxes = 0.0
        for item in self.items:
            tax_categories = TaxCategory.get_taxes()
            for tax_category in tax_categories:
                if item.product.category_id == tax_category.category_id:
                    taxes += item.sub_total() * tax_category.tax_rate
        
        return taxes
    
    def get_total(self):
        """
        Total price of cart items
        """
        return self.sub_total() + self.get_taxes()


class CartItem(models.Model):
    """
    Represents customer's product in basket
    """
    cart = models.ForeignKey(Cart, related_name='items')
    product = models.ForeignKey('catalog.Product')
    quantity = models.IntegerField(default=1)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'sales_cart_item'
        ordering = ('id',)
        verbose_name_plural = 'Cart Items'
    
    def sub_total(self, currency):
        return self.product.price * self.quantity
    

class Order(models.Model):
    """
    Represents customer's order
    """
    customer = models.ForeignKey(settings.AUTH_USER_MODEL) # Referencing custom defined model in settings file
    currency = models.ForeignKey('finance.Currency')
    sub_total = models.DecimalField(max_digits=9, decimal_places=2)
    taxes = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    

class OrderItem(models.Model):
    """
    Represents a purchase product
    """
    order = models.ForeignKey(Order)
    product = models.ForeignKey('catalog.Product')
    price = models.DecimalField(max_digits=9, decimal_places=2, help_text='Unit price of the product')
    quantity = models.IntegerField()
    tax_rate = models.FloatField(default=0.0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'sales_order_item'
        verbose_name_plural = 'Order Items'