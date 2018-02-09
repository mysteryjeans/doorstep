from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string

from doorstep.geo.models import Address
from doorstep.catalog.models import Product
from doorstep.financial.models import Currency, Tax


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

    def get_items_with_taxes(self):
        """
        Fetch cart items with products and taxes
        """
        return self.items.prefetch_related('product', 'product__tax').all()

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
        if product.tax:
            return product.tax.calculate(product.price, self.quantity)

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
    CREDIT_CARD = 'CC'
    PURCHASE_ORDER = 'PO'
    ALL = ((COD, 'Cash On Delivery'),
           (CHECK, 'Check / Money Order'),
           (CREDIT_CARD, 'Credit Card'),
           (PURCHASE_ORDER, 'Purchase Order'))
    ALL_METHODS = dict(ALL)

    code = models.CharField(primary_key=True, max_length=2, choices=ALL)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        db_table = 'sales_payment_method'
        verbose_name_plural = 'Payment Methods'

    def __unicode__(self):
        return '%s: %s' % (self.code, self.name)

    @classmethod
    def get_all(cls):
        """
        Returns list of active/supported payments method
        """
        return list(cls.objects.filter(is_active=True))


class OrderManager(models.Manager):
    def place(self, cart_id, billing_address_id, shipping_address_id, payment_method,
              po_number, currency_code, user, username):
        cart = Cart.get_cart(cart_id)
        billing_address = Address.objects.get(id=billing_address_id)
        shipping_address = Address.objects.get(id=shipping_address_id)
        payment_method = PaymentMethod.objects.get(code=payment_method)
        currency = Currency.objects.get(code=currency_code)
        charge_amount = float(cart.get_total())
        charge_amount *= float(currency.exchange_rate)
        receipt_code = get_random_string(20)  # allows secure access to order receipt

        order = self.create(customer=user,
                            currency=currency,
                            sub_total=cart.get_sub_total(),
                            shipping_cost=cart.get_shipping_cost(),
                            taxes=cart.get_taxes(),
                            total=cart.get_total(),
                            exchange_rate=currency.exchange_rate,
                            charge_amount=charge_amount,
                            order_status=self.model.ORDER_PENDING,
                            payment_method=payment_method,
                            payment_status=self.model.PAYMENT_PENDING,
                            po_number=po_number,
                            shipping_status=self.model.SHIPPING_PENDING,
                            billing_address=billing_address,
                            shipping_address=shipping_address,
                            receipt_code=receipt_code,
                            updated_by=username,
                            created_by=username)

        for item in cart.get_items_with_taxes():
            product = item.product

            if product.tax:
                tax_rate = product.tax.rate
                tax_method = product.tax.method
            else:
                tax_rate = 0.0
                tax_method = None

            OrderItem.objects.create(order=order,
                                     product=product,
                                     price=product.price,
                                     quantity=item.quantity,
                                     taxes=item.get_taxes(),
                                     sub_total=item.get_sub_total(),
                                     total=item.get_total(),
                                     tax_rate=tax_rate,
                                     tax_method=tax_method,
                                     updated_by=username,
                                     created_by=username)

        return order


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

    # Referencing custom defined model in settings file
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    currency = models.ForeignKey(Currency)
    sub_total = models.DecimalField(max_digits=9, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=9, decimal_places=2)
    taxes = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    refunded_amount = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    exchange_rate = models.FloatField(default=1)
    charge_amount = models.DecimalField(max_digits=9, decimal_places=2,
                                        help_text='Order total amount in user prefered currency that has been charged.')
    order_status = models.CharField(max_length=2, choices=ORDER_STATUSES)
    payment_method = models.ForeignKey(PaymentMethod, db_column='payment_method_code')
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUSES)
    po_number = models.CharField(max_length=100, null=True, blank=True,
                                 help_text='Purchase Order number')
    shipping_status = models.CharField(max_length=2, choices=SHIPPING_STATUSES)
    billing_address = models.ForeignKey(Address, related_name='billing_orders')
    shipping_address = models.ForeignKey(Address, related_name='shipping_orders', null=True, blank=True)
    receipt_code = models.CharField(max_length=100, help_text="Random code generate for each order for secure access.")
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    objects = OrderManager()

    def __unicode__(self):
        return unicode(self.id)

    def get_order_status(self):
        return next((status[1] for status in self.ORDER_STATUSES if status[0] == self.order_status), None)

    def get_payment_status(self):
        return next((status[1] for status in self.PAYMENT_STATUSES if status[0] == self.payment_status), None)

    def get_shipping_status(self):
        return next((status[1] for status in self.SHIPPING_STATUSES if status[0] == self.shipping_status), None)


class OrderItem(models.Model):
    """
    Represents a purchase product
    """
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey('catalog.Product')
    price = models.DecimalField(max_digits=9, decimal_places=2, help_text='Unit price of the product')
    quantity = models.IntegerField()
    taxes = models.DecimalField(max_digits=9, decimal_places=2)
    sub_total = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    tax_rate = models.FloatField(default=0.0)
    tax_method = models.CharField(max_length=2, choices=Tax.TAX_METHODS, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        db_table = 'sales_order_item'
        verbose_name_plural = 'Order Items'
