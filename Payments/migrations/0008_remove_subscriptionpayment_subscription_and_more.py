# Generated by Django 5.1.6 on 2025-04-16 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0007_subscriptionplan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptionpayment',
            name='subscription',
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
