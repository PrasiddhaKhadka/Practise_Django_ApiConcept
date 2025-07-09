from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = DefaultRouter()
router.register(r'product', views.ProductViewSet, basename='product')
router.register(r'collection', views.CollectionViewSet, basename='collection')


product_router = routers.NestedDefaultRouter(router, r'product', lookup='product')
product_router.register(r'review', views.ReviewViewSet, basename='product-review')



urlpatterns = router.urls + product_router.urls