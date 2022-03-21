from dataclasses import fields
from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']

    product_count = serializers.IntegerField(read_only=True)
# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


# class ProductSerializer(serializers.Serializer):
#     """ Here what information want to show to the outer world/User
#     Return from an API doesn't necessariy need to have all fields from model, Because in models we have sometimes sensitive information also calld a internal representation and in api view we have called external representation that client see,
#     from product model lets return an id, title and unit_price.
#     """
#     # is just like a models fields
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(
#         max_digits=6, decimal_places=2, source='unit_price')
#     price_with_tax = serializers.SerializerMethodField(
#         method_name='calculate_tax')
#     # collection = serializers.StringRelatedField()
#     collection = serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(),
#         view_name='collection-detail'
#     )

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory',
                  'unit_price', 'price_with_tax', 'collection']

    # You can override this also by changing its attributes, or add it like price_with tax

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        # need to change in decimal because 0.18 is a flota
        return float("{:.2f}".format(product.unit_price * Decimal(1.18)))

    # def validate(self, data): #it just an example it not related any above this
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('password do not match')
    #     return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
