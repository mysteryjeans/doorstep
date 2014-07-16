from django.db import models
from django.conf import settings

from doorsale.geo.models import Address
from doorsale.catalog.models import Product
from doorsale.financial.models import Currency, TaxRate


class Cart(models.Model):
    """
    Represents customer's shopping basket
    """
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    def get_sub_total(self):
        """
        Sub total of cart items (without taxes)
        """
        sub_total = 0.0
        for item in self.items.all():
            sub_total += item.get_sub_total()
        
        return sub_total
    
    def get_taxes(self):
        """
        Total taxes applied on cart items
        """
        taxes = 0.0
        for item in self.get_items():
            taxes += item.get_taxes()
        
        return taxes

    def get_shipping_cost(self):
        """
        Return total cost for shipping
        """
        shipping_cost = 0.0
        for item in self.get_items():
            shipping_cost += item.get_shipping_cost()

        return shipping_cost
    
    def get_total(self):
        """
        Total price of cart items with taxes
        """
        return float(self.get_sub_total() + self.get_taxes() + self.get_shipping_cost())
    
    def get_items_count(self):
        """
        Returns total number of items
        """
        items_count = 0
        for item in self.get_items():
            items_count += item.quantity
        
        return items_count
    
    def add_item(self, product_id, quantity, user):
        """
        Add or augment quantity of product
        """
        if self.items.filter(product_id=product_id):
            item = self.items.get(product_id=product_id)
            item.quantity += quantity
            item.save()
            return item
        
        item = self.items.create(product_id=product_id,
                                 quantity=quantity,
                                 updated_by=str(user),
                                 created_by=str(user))
        
        return item
    
    def remove_item(self, product_id):
        """
        Remove an item from cart
        """
        try:
            cart_item = self.items.get(product_id=product_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass

    def remove_all_items(self):
        """
        Remove all items form cart
        """
        for item in self.get_items():
            item.delete()

    def update_item(self, product_id, quantity):
        """
        Update item quantity in database
        """
        self.items.filter(product_id=product_id).update(quantity=quantity)

    def get_items(self):
        """
        Fetch cart items with products and pics
        """
        return self.items.prefetch_related('product', 'product__pics').all()
    
    @classmethod
    def get_cart(cls, cart_id=None):
        """
        Returns existing cart or creates new one
        """
        if cart_id:
            return cls.objects.get(id=cart_id)
        
        return cls.objects.create()
        


class CartItem(models.Model):
    """
    Represents customer's product in basket
    """
    cart = models.ForeignKey(Cart, related_name='items')
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'sales_cart_item'
        ordering = ('id',)
        verbose_name_plural = 'Cart Items'
        unique_together = ('cart', 'product',)
    
    def get_sub_total(self):
        """
        Sub total of cart item (without taxes)
        """
        return float(self.product.price) * self.quantity
    
    def get_taxes(self):
        """
        Total taxes applied on cart item
        """
        product = self.product
        if product.tax_rate:
            return product.tax_rate.calculate(product.price, self.quantity)
        
        return 0.0

    def get_shipping_cost(self):
        """
        Returns total shipping cost
        """
        product = self.product
        if product.is_free_shipping:
            return 0.0

        return float(product.shipping_cost) * float(self.quantity)
    
    def get_total(self):
        """
        Total price of cart item with taxes
        """
        return self.get_sub_total() + self.get_taxes() + self.get_shipping_cost()


class PaymentMethod(models.Model):
    """
    Represents payment methods for order
    """
    # Payment methods
    COD = 'CO'
    CHECK = 'CH'
    CREDIT = 'CC'
    PURCHASE = 'PO'
    ALL = ((COD, 'Cash On Delivery'),
           (CHECK, 'Check / Money Order'),
           (CREDIT, 'Credit Card'),
           (PURCHASE, 'Purchase Order'))
    
    code = models.CharField(primary_key=True, max_length=2, choices=ALL)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'sales_payment_method'
        verbose_name_plural = 'Payment Methods'


class Order(models.Model):
    """
    Represents customer's order
    """
    # Order statuses
    ORDER_PENDING = 'PE'
    ORDER_PROCESSING = 'PR'
    ORDER_COMPLETE = 'CO'
    ORDER_CANCELLED = 'CA'
    ORDER_STATUSES = ((ORDER_PENDING, 'Pending'),
                      (ORDER_PROCESSING, 'Processing'),
                      (ORDER_COMPLETE, 'Complete'),
                      (ORDER_CANCELLED, 'Cancelled'))
    
    # Payment statuses
    PAYMENT_PENDING = 'PE'
    PAYMENT_AUTHORIZED = 'AU'
    PAYMENT_PAID = 'PA'
    PAYMENT_PARTIALLY_REFUNDED = 'PR'
    PAYMENT_REFUNDED = 'RE'
    PAYMENT_VOID = 'VO'
    PAYMENT_STATUSES = ((PAYMENT_PENDING, 'Pending'),
                        (PAYMENT_AUTHORIZED, 'Authorized'),
                        (PAYMENT_PAID, 'Paid'),
                        (PAYMENT_PARTIALLY_REFUNDED, 'Partially Refunded'),
                        (PAYMENT_REFUNDED, 'Refunded'),
                        (PAYMENT_VOID, 'Void'))
    
    # Shipping statuses
    SHIPPING_NOT_REQUIRED = 'NR'
    SHIPPING_PENDING = 'PE'
    SHIPPING_PARTIALLY_SHIPPED = 'PS'
    SHIPPING_SHIPPED = 'SH'
    SHIPPING_DELIVERED = 'DE'
    SHIPPING_STATUSES = ((SHIPPING_NOT_REQUIRED, 'Not Required'),
                         (SHIPPING_PENDING, 'Pending'),
                         (SHIPPING_PARTIALLY_SHIPPED, 'Partially Shipped'),
                         (SHIPPING_SHIPPED, 'Shipped'),
                         (SHIPPING_DELIVERED, 'Delivered'))
    
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True) # Referencing custom defined model in settings file
    currency = models.ForeignKey(Currency)
    sub_total = models.DecimalField(max_digits=9, decimal_places=2)
    taxes = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    refunded_amount = models.DecimalField(max_digits=9, decimal_places=2)
    currency_rate = models.FloatField(default=1)
    order_status = models.CharField(max_length=2, choices=ORDER_STATUSES)
    payment_method = models.ForeignKey(PaymentMethod, db_column='payment_method_code')
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUSES)
    po_number = models.CharField(max_length=100, null=True, blank=True,
                                 help_text='Purchase Order number')
    shipping_status = models.CharField(max_length=2, choices=SHIPPING_STATUSES)
    billing_address = models.ForeignKey(Address, related_name='billing_orders')
    shipping_address = models.ForeignKey(Address, related_name='shipping_orders', null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.id


class OrderItem(models.Model):
    """
    Represents a purchase product
    """
    order = models.ForeignKey(Order)
    product = models.ForeignKey('catalog.Product')
    price = models.DecimalField(max_digits=9, decimal_places=2, help_text='Unit price of the product')
    quantity = models.IntegerField()
    taxes = models.DecimalField(max_digits=9, decimal_places=2)
    sub_total = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    tax_rate = models.FloatField(default=0.0)
    tax_method = models.CharField(max_length=2, choices=TaxRate.TAX_METHODS)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'sales_order_item'
        verbose_name_plural = 'Order Items'
        