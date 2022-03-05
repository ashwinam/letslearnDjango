from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

# Register your models here.


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = ['title', 'slug'] # it gives only this fields
    # exclude = ['title'] # remove the particular field from forms
    # readonly_fields = ['title'] # just read the field
    search_fields = ['title__istartswith']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }  # caution : it breaks if we try to chamge the slug field
    actions = ['clear_inventory']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']  # edit on list page, Changes in one go
    list_per_page = 10  # it works like pagination
    list_select_related = ['collection']  # preload

    def collection_title(self, Product):
        return Product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, Product):
        if Product.inventory < 10:
            return 'Low'
        return 'OK'
# admin.site.register(models.Product, ProductAdmin) # write this way or using decorator like above one

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} Products were succesfully updated.",
            messages.ERROR
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # url = reverse('admin:app_model_page')# basic syntax for reverse links in a dynamic way
        url = (reverse('admin:store_product_changelist') + '?' + urlencode({
            'collection__id': str(collection.id)
        }))
        return format_html('<a href={}>{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

# admin.site.register(models.Customer, CustomerAdmin)


class OrderItemInline(admin.TabularInline):  # 2nd option is stacked Inline
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    extra = 0
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', 'customer']
