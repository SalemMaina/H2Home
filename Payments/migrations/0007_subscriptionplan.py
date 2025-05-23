# Generated by Django 5.1.6 on 2025-04-16 08:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0006_remove_subscription_plan_delete_subscriptionplan'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interval', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], max_length=20)),
                ('is_active', models.BooleanField(default=False)),
                ('paystack_plan_code', models.CharField(blank=True, help_text='Set automatically after creating plan in Paystack dashboard', max_length=50)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Subscription Plan',
                'verbose_name_plural': 'Subscription Plans',
            },
        ),
    ]
