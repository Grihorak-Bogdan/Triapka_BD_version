# Generated by Django 4.2.7 on 2024-02-06 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_size_remove_products_quantity_alter_products_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='l_count',
        ),
        migrations.RemoveField(
            model_name='products',
            name='m_count',
        ),
        migrations.RemoveField(
            model_name='products',
            name='s_count',
        ),
        migrations.RemoveField(
            model_name='products',
            name='size',
        ),
        migrations.RemoveField(
            model_name='products',
            name='xl_count',
        ),
        migrations.RemoveField(
            model_name='products',
            name='xs_count',
        ),
        migrations.RemoveField(
            model_name='products',
            name='xxl_count',
        ),
    ]
