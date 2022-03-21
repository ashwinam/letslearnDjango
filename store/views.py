from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from store import serializer
from .pagination import DefaultPagination
from .filter import ProductFilter
from .models import Collection, OrderItem, Product, Review
from.serializer import CollectionSerializer, ProductSerializer, ReviewSerializer


# def product_list(request):
#     return HttpResponse('OK')

# @api_view(['GET', 'POST'])  # by default it set GET method
# def product_list(request):
#     if request.method == 'GET':  # request of rest_framework
#         queryset = Product.objects.select_related('collection').all()
#         serialier = ProductSerializer(
#             queryset, many=True, context={'request': request})
#         return Response(serialier.data)  # response of rest_framework
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serialier.save()
#         # print(serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view()
# def product_detail(request, id):
#     try:
#         product = Product.objects.get(pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     except Product.DoesNotExist:
#         # right way to use this is import status
#         return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(
            product_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(product_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it include one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------Class-Based Views code---------------------

# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serialier = ProductSerializer(
#             queryset, many=True, context={'request': request})
#         return Response(serialier.data)  # response of rest_framework

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ProductDetail(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# -------------------Generic view-------------------


class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    # dont create a object just pass a reference
    serializer_class = ProductSerializer
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()

    # def get_serializer_class(self):
    #     return ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        product_count=Count('products')).all()
    serializer_class = CollectionSerializer


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(product_count=Count('products'))
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(product_count=Count('products')), pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it include one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------------------View sets---------------------------------------------------
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'unit_price', 'last_update']
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(
    #             collection_id=collection_id
    #         )
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = queryset = Collection.objects.annotate(
        product_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Collection.objects.annotate(product_count=Count('products')).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it include one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
