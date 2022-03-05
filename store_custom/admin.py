from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem


# Register your models here.
class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


# Create New Product Admin that extend Generic Product Admin for our reusable apps.
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]

# So we have New Product Admin we need to unregister old ones & register New product admin


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
