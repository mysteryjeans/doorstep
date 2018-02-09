# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('pic', models.ImageField(null=True, upload_to='images/catalog/categories', blank=True)),
                ('tags', models.CharField(help_text='Comma-delimited set of SEO keywords for meta tag', max_length=100, null=True, blank=True)),
                ('display_order', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(related_name='sub_categories', blank=True, to='catalog.Category', null=True)),
            ],
            options={
                'ordering': ('display_order', 'id'),
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('part_number', models.CharField(help_text='Manufacturer part number', max_length=50, null=True, blank=True)),
                ('sku', models.CharField(max_length=50, null=True, verbose_name='SKU', blank=True)),
                ('gtin', models.CharField(help_text='Global Trade Item Number (GTIN)', max_length=50, null=True, verbose_name='GTIN', blank=True)),
                ('gist', models.CharField(help_text='Short description of the product', max_length=500, null=True, blank=True)),
                ('description', models.TextField(help_text='Full description displayed on the product page', null=True, blank=True)),
                ('price', models.DecimalField(help_text='Per unit price', max_digits=9, decimal_places=2)),
                ('old_price', models.DecimalField(default=0.0, max_digits=9, decimal_places=2)),
                ('cost', models.DecimalField(default=0.0, help_text='Per unit cost', max_digits=9, decimal_places=2)),
                ('shipping_cost', models.DecimalField(default=0.0, help_text='Shipping cost per unit', max_digits=9, decimal_places=2)),
                ('quantity', models.IntegerField(help_text='Stock quantity')),
                ('is_active', models.BooleanField(default=True, help_text='Product is available for listing and sale')),
                ('is_bestseller', models.BooleanField(default=False, help_text='It has been best seller')),
                ('is_featured', models.BooleanField(default=False, help_text='Promote this product on main pages')),
                ('is_free_shipping', models.BooleanField(default=False, help_text='No shipping charges')),
                ('tags', models.CharField(help_text='Comma-delimited set of SEO keywords for meta tag', max_length=250, null=True, blank=True)),
                ('weight', models.FloatField(default=0)),
                ('length', models.FloatField(default=0)),
                ('width', models.FloatField(default=0)),
                ('height', models.FloatField(default=0)),
                ('updated_by', models.CharField(max_length=100)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('brand', models.ForeignKey(help_text='Manufacturer', to='catalog.Manufacturer')),
                ('category', models.ForeignKey(to='catalog.Category')),
                ('tax', models.ForeignKey(blank=True, to='financial.Tax', help_text='Tax applied on this product, if tax exempt select none', null=True)),
            ],
            options={
                'ordering': ('id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductPic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.ImageField(upload_to='images/catalog/products')),
                ('display_order', models.IntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('product', models.ForeignKey(related_name='pics', to='catalog.Product')),
            ],
            options={
                'ordering': ('display_order', 'id'),
                'db_table': 'catalog_product_pic',
                'verbose_name_plural': 'Product Pics',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductSpec',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=250)),
                ('display_order', models.IntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('product', models.ForeignKey(related_name='specs', to='catalog.Product')),
            ],
            options={
                'ordering': ('display_order', 'id'),
                'db_table': 'catalog_product_spec',
                'verbose_name_plural': 'Product Specs',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='productspec',
            unique_together=set([('product', 'name')]),
        ),
    ]
