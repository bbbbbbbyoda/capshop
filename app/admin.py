from django.contrib import admin
from .models import Brand, Product, Order, OrderDetail, Price, Stock, DetailPhotos


class DetailPhotoInline(admin.TabularInline):
    model = DetailPhotos


class PriceInline(admin.TabularInline):
    model = Price


class CapAdmin(admin.ModelAdmin):
    inlines = [
        DetailPhotoInline,
        PriceInline,
    ]
    list_display = ['id', 'name', 'is_active', 'cover_image']


admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Price)
admin.site.register(Stock)
admin.site.register(DetailPhotos)










