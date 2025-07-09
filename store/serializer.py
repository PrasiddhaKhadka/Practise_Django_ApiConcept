from rest_framework.serializers import ModelSerializer
from store.models import Product, Collection, Review

class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'label']

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price','slug', 'description']

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'customer', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create( product_id=product_id, **validated_data)