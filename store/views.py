from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from store.filters import ProductFilter
from store.models import Product, Collection, Review
from store.pagination import DefaultPagination
from store.serializer import ProductSerializer, CollectionSerializer, ReviewSerializer



class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
   

class ProductViewSet(ModelViewSet):
   queryset = Product.objects.all()
   serializer_class = ProductSerializer
   filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
   filterset_fields = ['collection_id', 'price', 'inventory']
   search_fields = ['title']
   ordering_fields = ['price']
   pagination_class = DefaultPagination
   filterset_class = ProductFilter
   


class ReviewViewSet(ModelViewSet):
   
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'product_id': self.kwargs['product_pk']
        }
    