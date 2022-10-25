# Generated by Django 4.1.2 on 2022-10-24 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_product_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prices', to='app.product', verbose_name='Продукт'),
        ),
    ]
