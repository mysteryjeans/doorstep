# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardIssuer',
            fields=[
                ('descriptor', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'payments_card_issuer',
                'verbose_name_plural': 'Card Issuers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('name', models.CharField(help_text='Payment processing gateway.', max_length=10, serialize=False, primary_key=True, choices=[('PP', 'PayPal'), ('ST', 'Stripe'), ('AP', 'Amazon Payments')])),
                ('account', models.CharField(help_text='Account name of gateway for reference.', max_length=100)),
                ('is_active', models.BooleanField(default=False, help_text='Gateway active for customer to buy through it.')),
                ('is_sandbox', models.BooleanField(default=False, help_text='Sandbox mode for testing & debugging.')),
                ('accept_credit_card', models.BooleanField(default=False, help_text='Process credit card payments.')),
                ('accept_account', models.BooleanField(default=False, help_text="Process payments with customer's existing accounts on gateway, like PayPal account.")),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GatewayParam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Gateway settings parameter name.', max_length=250)),
                ('value', models.CharField(help_text='Gateway settings parameter value.', max_length=500)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('gateway', models.ForeignKey(related_name='params', to='payments.Gateway')),
            ],
            options={
                'db_table': 'payments_gateway_param',
                'verbose_name_plural': 'Gateway Params',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=250)),
                ('error_message', models.CharField(max_length=1000)),
                ('status', models.CharField(max_length=100, choices=[('PE', 'Pending'), ('PR', 'Processing'), ('AP', 'Approved'), ('FA', 'Failed'), ('RE', 'Refunded')])),
                ('currency', models.CharField(max_length=3)),
                ('amount', models.DecimalField(max_digits=9, decimal_places=2)),
                ('refund_amount', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('gateway', models.ForeignKey(to='payments.Gateway')),
                ('order', models.ForeignKey(to='sales.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionParam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Transaction parameter name.', max_length=100)),
                ('value', models.CharField(help_text='Transaction parameter value.', max_length=250)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('transaction', models.ForeignKey(related_name='params', to='payments.Transaction')),
            ],
            options={
                'db_table': 'payments_transaction_param',
                'verbose_name_plural': 'Transaction Params',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='transactionparam',
            unique_together=set([('transaction', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='gatewayparam',
            unique_together=set([('gateway', 'name')]),
        ),
    ]
