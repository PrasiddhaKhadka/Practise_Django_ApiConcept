from django.contrib import admin,messages
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse
from . import models
from tags.models import Tag

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['label','products_count']
    search_fields = ['label__istartswith']
    list_filter = ['label']
    list_per_page = 10
    
    def get_queryset(self, request):
        return models.Collection.objects.prefetch_related('products').annotate(products_count=Count('products'))
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?collection_id__exact=' + str(collection.id)
        return format_html('<a href="{}">{}</a>',url,collection.products.count())
    

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ['title', 'price','collection','inventory_status']
    list_filter = ['collection','price']
    list_editable = ['price']
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title__istartswith','collection__label__istartswith']
    prepopulated_fields = {
        'slug': ['title']
    }

    autocomplete_fields = ['collection']


    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 1:
            return 'Out of stock'
        return product.inventory
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(request,f'{update_count} products were updated',messages.ERROR)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['phone','membership','birth_date']
    list_filter = ['membership']
    list_per_page = 10
    search_fields = ['phone_no__istartswith']

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at','customer']
    list_per_page = 10
    search_fields = ['customer__phone__istartswith']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity']
    list_per_page = 10
    autocomplete_fields = ['order','product']
    search_fields = ['product__title__istartswith']


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id','created_at']
    list_per_page = 10
    search_fields = ['cart_id__istartswith']


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart','product','quantity']
    list_per_page = 10
    autocomplete_fields = ['cart','product']
    search_fields = ['product__title__istartswith']

