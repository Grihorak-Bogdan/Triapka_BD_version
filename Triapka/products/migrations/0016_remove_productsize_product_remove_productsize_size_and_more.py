# Generated by Django 4.2.7 on 2024-01-12 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_alter_productimage_product_alter_productsize_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productsize',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productsize',
            name='size',
        ),
        migrations.AddField(
            model_name='products',
            name='l_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='products',
            name='m_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='products',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='products',
            name='s_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='products',
            name='size',
            field=models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Extra Extra Large')], default='XS', max_length=3),
        ),
        migrations.AddField(
            model_name='products',
            name='xl_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='products',
            name='xs_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='products',
            name='xxl_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.products'),
        ),
        migrations.AlterField(
            model_name='products',
            name='gender',
            field=models.CharField(choices=[('Man', 'Male'), ('Woman', 'Female'), ('Unisex', 'Unisex')], default='Unisex', max_length=6),
        ),
        migrations.DeleteModel(
            name='AllSize',
        ),
        migrations.DeleteModel(
            name='ProductSize',
        ),
    ]
