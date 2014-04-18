from django.db import models

from doorsale.financial.models import TaxRate

class Manufacturer(models.Model):
    """
    Represents a Manufacturer
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='images/catalog/manufacturers', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        ordering = ('id',)
    
    def __unicode__(self):
        return self.name


class Category(models.Model):
    """
    Represents a Category for Products
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='images/catalog/categories', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    tags = models.CharField(max_length=100, null=True, blank=True, help_text='Comma-delimited set of SEO keywords for meta tag')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        ordering = ('display_order', 'id',)
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        if self.parent:
            return u"%s > %s" % (self.parent, self.name)

        return self.name


class Product(models.Model):
    """
    Represents a Product
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    brand = models.ForeignKey(Manufacturer, help_text='Manufacturer')
    part_number = models.CharField(max_length=50, null=True, blank=True, help_text='Manufacturer part number')
    sku = models.CharField(max_length=50, null=True, blank=True)
    gtin = models.CharField(max_length=50, null=True, blank=True, 
                            help_text='Global Trade Item Number (GTIN)')
    categories = models.ManyToManyField(Category)
    gist = models.CharField(max_length=500, null=True, blank=True, help_text='Short description of the product')
    description = models.TextField(null=True, blank=True, help_text='Full description displayed on the product page')
    price = models.DecimalField(max_digits=9, decimal_places=2, help_text='Per unit price')
    old_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.0)
    cost = models.DecimalField(max_digits=9, decimal_places=2, default=0.0, help_text='Per unit cost')
    shipping_cost = models.DecimalField(max_digits=9, decimal_places=2, default=0.0, help_text='Shipping cost per unit')
    quantity = models.IntegerField(help_text='Stock quantity')
    is_active = models.BooleanField(default=True, help_text='Product is available for listing and sale')
    is_bestseller = models.BooleanField(default=False, help_text='It has been best seller')
    is_featured = models.BooleanField(default=False, help_text='Promote this product on main pages')
    is_free_shipping = models.BooleanField(default=False, help_text='No shipping charges')
    tax_rate = models.ForeignKey(TaxRate, null=True, blank=True, help_text='Tax applied on this product, if tax exempt select none')
    tags = models.CharField(max_length=250, null=True, blank=True, help_text='Comma-delimited set of SEO keywords for meta tag')
    weight = models.FloatField(default=0)
    length = models.FloatField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return self.name


class ProductSpec(models.Model):
    """
    Represents product specification attribute
    """
    product = models.ForeignKey(Product, related_name='specs')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=250)
    display_order = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        db_table = 'catalog_product_spec'
        ordering = ('display_order', 'id',)
        unique_together = ('product', 'name',)
        verbose_name_plural = 'Product Specs'
    
    def __unicode__(self):
        return u'%s: %s' % (self.name, self.value)


class ProductPic(models.Model):
    """
    Represents product picture
    """
    product = models.ForeignKey(Product, related_name='pics')
    url = models.ImageField(upload_to="images/catalog/products")
    display_order = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        db_table = 'catalog_product_pic'
        ordering = ('display_order', 'id')
        verbose_name_plural = 'Product Pics'

    def __unicode__(self):
        return u'%s [Pic #id %s]' % (self.product, self.id)


        


