# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.core.management import call_command


def load_data(apps, schema_editor):
    call_command('loaddata', 'initial_data', app_label='sales', verbosity=0)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
        ('geo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financial', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('cart', models.ForeignKey(related_name='items', to='sales.Cart')),
                ('product', models.ForeignKey(to='catalog.Product')),
            ],
            options={
                'ordering': ('id',),
                'db_table': 'sales_cart_item',
                'verbose_name_plural': 'Cart Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sub_total', models.DecimalField(max_digits=9, decimal_places=2)),
                ('shipping_cost', models.DecimalField(max_digits=9, decimal_places=2)),
                ('taxes', models.DecimalField(max_digits=9, decimal_places=2)),
                ('total', models.DecimalField(max_digits=9, decimal_places=2)),
                ('refunded_amount', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('exchange_rate', models.FloatField(default=1)),
                ('charge_amount', models.DecimalField(help_text='Order total amount in user prefered currency that has been charged.', max_digits=9, decimal_places=2)),
                ('order_status', models.CharField(max_length=2, choices=[('PE', 'Pending'), ('PR', 'Processing'), ('CO', 'Complete'), ('CA', 'Cancelled')])),
                ('payment_status', models.CharField(max_length=2, choices=[('PE', 'Pending'), ('AU', 'Authorized'), ('PA', 'Paid'), ('PR', 'Partially Refunded'), ('RE', 'Refunded'), ('VO', 'Void')])),
                ('po_number', models.CharField(help_text='Purchase Order number', max_length=100, null=True, blank=True)),
                ('shipping_status', models.CharField(max_length=2, choices=[('NR', 'Not Required'), ('PE', 'Pending'), ('PS', 'Partially Shipped'), ('SH', 'Shipped'), ('DE', 'Delivered')])),
                ('receipt_code', models.CharField(help_text='Random code generate for each order for secure access.', max_length=100)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('billing_address', models.ForeignKey(related_name='billing_orders', to='geo.Address')),
                ('currency', models.ForeignKey(to='financial.Currency')),
                ('customer', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(help_text='Unit price of the product', max_digits=9, decimal_places=2)),
                ('quantity', models.IntegerField()),
                ('taxes', models.DecimalField(max_digits=9, decimal_places=2)),
                ('sub_total', models.DecimalField(max_digits=9, decimal_places=2)),
                ('total', models.DecimalField(max_digits=9, decimal_places=2)),
                ('tax_rate', models.FloatField(default=0.0)),
                ('tax_method', models.CharField(blank=True, max_length=2, null=True, choices=[('PE', 'Percentage'), ('FI', 'Fixed')])),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('order', models.ForeignKey(related_name='items', to='sales.Order')),
                ('product', models.ForeignKey(to='catalog.Product')),
            ],
            options={
                'db_table': 'sales_order_item',
                'verbose_name_plural': 'Order Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('code', models.CharField(max_length=2, serialize=False, primary_key=True, choices=[('CO', 'Cash On Delivery'), ('CH', 'Check / Money Order'), ('CC', 'Credit Card'), ('PO', 'Purchase Order')])),
                ('name', models.CharField(unique=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'sales_payment_method',
                'verbose_name_plural': 'Payment Methods',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.ForeignKey(to='sales.PaymentMethod', db_column='payment_method_code'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(related_name='shipping_orders', blank=True, to='geo.Address', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together=set([('cart', 'product')]),
        ),
        migrations.RunPython(load_data),
    ]
