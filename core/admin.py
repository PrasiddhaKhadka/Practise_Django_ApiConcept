from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from tags.models import TaggedItem
from store.admin import ProductAdmin
from store.models import Product

# Register your models here.
class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']
    extra = 0 
    min_num = 1
    max_num = 10


class CustomProductAdmin(ProductAdmin):
    inlines = [TaggedItemInline]

admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)