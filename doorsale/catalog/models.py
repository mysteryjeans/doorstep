from django.db import models


class Manufacturer(models.Model):
    """
    Represents a Manufacturer
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='images/catalog/manufacturers')
    is_active = models.BooleanField(default=True)
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    """
    Represents a Category for Products
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='images/catalog/categories')
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
    brand = models.ForeignKey(Manufacturer)
    sku = models.CharField(max_length=50, null=True, blank=True)
    gist = models.CharField(max_length=500, null=True, blank=True, help_text='Short description of the Product')
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    rating  = models.FloatField(default=0.0)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    category = models.ForeignKey(Category)
    tags = models.CharField(max_length=250, null=True, blank=True, help_text='Comma-delimited set of SEO keywords for meta tag')
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
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='specs')
    display_order = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        db_table = 'catalog_product_spec'
        ordering = ('display_order', 'id',)
        unique_together = ('name', 'product',)
        verbose_name_plural = 'Product Specs'
    
    def __unicode__(self):
        return u'%s: %s' % (self.name, self.value)


class ProductPic(models.Model):
    """
    Represents product picture
    """
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='pics')
    url = models.ImageField(upload_to="images/catalog/products")
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        db_table = 'catalog_product_pic'
        unique_together = ('name', 'id',)
        verbose_name_plural = 'Product Pics'

    def __unicode__(self):
        return self.name



        


