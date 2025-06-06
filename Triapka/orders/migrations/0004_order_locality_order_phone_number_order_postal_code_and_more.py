# Generated by Django 4.2.7 on 2024-08-06 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='locality',
            field=models.CharField(default='Невідомо', max_length=128),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(default='0000000000', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(default='00000', max_length=12),
        ),
        migrations.AddField(
            model_name='order',
            name='region',
            field=models.CharField(default='Невідомо', max_length=128),
        ),
    ]
