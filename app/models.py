from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField

User = get_user_model()


class Brand(models.Model):
    name = models.CharField(
        verbose_name=_('Имя'),
        max_length=125
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'


class Product(models.Model):
    name = models.CharField(
        max_length=125,
        verbose_name=_('Имя')
    )
    description = models.CharField(max_length=125)
    cover = models.ImageField(
        upload_to='media/images',
        verbose_name=_('Главное фото')
    )
    brand = models.ManyToManyField(
        Brand,
        verbose_name=_('Бренды'),
        related_name='products'
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата изменения'),
        auto_now=True
    )
    active = models.BooleanField(
        verbose_name=_('Данный товар активен'),
        default=True
    )

    def cover_image(self):
        return format_html(f'<img src="width:100px;height:150px"/>')

    @property
    def is_active(self):
        return self.active

    @property
    def price(self):
        return self.prices.get(is_active=True).value

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class DetailPhotos(models.Model):
    image = models.ImageField(
        verbose_name=_('Детальное фото'),
        upload_to='media/images',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name=_('Продукты'),
        related_name='photos'
    )

    class Meta:
        verbose_name = 'Детальное фото'
        verbose_name_plural = 'Детальные фото'


class Price(models.Model):
    value = models.DecimalField(
        verbose_name=_('Цена товара'),
        decimal_places=2,
        max_digits=12
    )
    start_date = models.DateTimeField(
        verbose_name=_('Дата старта цены')
    )
    end_date = models.DateTimeField(
        verbose_name=_('Дата конца цены'),
        default=datetime(year=2999, month=12, day=31, hour=12, second=59)
    )
    is_active = models.BooleanField(
        verbose_name=_('Актуальная цена'),
        default=False
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name=_('Продукт'),
        related_name='prices'
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата изменения'),
        auto_now=True
    )

    def save(self, *args, **kwargs):
        previos_price = self.cap.prices.filter(is_active=True).last()

        if previos_price is not None and self != previos_price:
            previos_price.is_active = False
            previos_price.end_date = self.start_date
            previos_price.save()

        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'


class Stock(models.Model):
    size = models.SmallIntegerField(
        verbose_name=_('Размер'),
        choices=(
            (1, 'S'),
            (2, 'M'),
            (3, 'L'),
            (4, 'XL'),
        ))
    color = ColorField(
        default='#FF0000',
        verbose_name=_('Цвет'),
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата поступления'),
    )
    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата нового поступления'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name=_('Продукт'),
        related_name='stocks'
    )

    def __str__(self):
        return f'{self.product}{self.size}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склад'


class Order(models.Model):
    status = models.BooleanField(
        verbose_name=_('Статус'),
        default=True)
    total = models.PositiveIntegerField(
        verbose_name=_('Сумма'),
        default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Пользователь'),
    )
    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Склад'),
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата утсановления статуса'),
    )
    update_date = models.DateTimeField(
        verbose_name=_('Дата изменения статуса'),
        auto_now=True)

    address = models.CharField(max_length=125)

    def __str__(self):
        return f'{self.stock}{self.user}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderDetail(models.Model):
    quantity = models.PositiveIntegerField(
        verbose_name=_('Количество'),
        default=0
    )
    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
        related_name='order_details',
        verbose_name=_('Склад')
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='order_details',
        verbose_name=_('Заказ')
    )

    class Meta:
        verbose_name = 'Детали заказа'
        verbose_name_plural = 'Детали заказа'


class Link(models.Model):
    url = models.URLField(
        verbose_name=_('Ссылка')
    )
    cover = models.ImageField(
        upload_to='media/image/',
        verbose_name=_('Изображение'))

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'
