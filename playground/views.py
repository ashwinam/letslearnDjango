from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q, F, Value, Func
from django.db.models.aggregates import Count, Min, Max, Avg, Sum
from store.models import Product, OrderItem, Order, Customer, Collection
from tags.models import TaggedItem


# pull data from db
# Trandform Data
# send emails and so on.


# def say_hello(request):
# here it takes request object
# return HttpResponse('hello World')
# Product.objects.all() # pulling all data from the product table
# Product.objects.get() # pulling single data
# Product.objects.filter() # filtering data

# query_set = Product.objects.all()  # it return the query set

# product = Product.objects.get(pk=0)  # it throws an exception
# try:
#     product = Product.objects.get(pk=0)
# except ObjectDoesNotExist:
#     pass

# # more cleaner way
# product = Product.objects.filter(pk=0).first()
# # here first method return none if object are not there

# # check the objects are there or not
# exists = Product.objects.filter(pk=0).exist()

# query_set = Product.objects.filter(unit_price__range=(20, 30))
# query_set = Product.objects.filter(collection__id__range=(1, 2, 3))
# query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
# OR
# query_set = Product.objects.filter(
# inventory__lt=10).filter(unit_price__lt=20)
# query_set = Product.objects.filter(
#     Q(inventory__lt=10) | Q(unit_price__lt=20))

# query_set = Product.objects.filter(inventory=F('unit_price'))
# query_set = Product.objects.filter(inventory=F('collection_id'))
# return render(request, 'hello.html', {'name': 'ashwin', 'products': list(query_set)})
# so for dynamic content we pass a dictionery as a third parameter

# def say_hello(request):
# query_set = Product.objects.values('id', 'title')
# Exercise: select products that have been ordered and sort them by title
# query_set = OrderItem.objects.values('product_id')
# query_set = Product.objects.filter(
#     id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
# query_set = Product.objects.only('id', 'title')
# query_set = Product.objects.select_related('collection').all()
# query_set = Product.objects.prefetch_related('promotions').all()
# query_set = Product.objects.prefetch_related(
#     'promotions').select_related('collection').all()

# Exercise: Get the last 5 orders with their customer and items(incl products)

# query_set = Order.objects.select_related(
#     'customer').prefetch_related('orderitem_set').order_by('-placed_at')[:5]

# result = Product.objects.aggregate(
#     count=Count('id'), min_price=Min('unit_price'))

# result = Product.objects.annotate(is_new=Value(True))
# result = Customer.objects.annotate(new_id=F('id')+1)

# Lets concat
# result = Customer.objects.annotate(full_name=Func(
# #     F('first_name'), Value(' '), F('last_name'), function='Concat'))
# result = Customer.objects.annotate(order_count=Count('order'))

# # Django coonvention create a reverse relationship automatically
# # return render(request, 'hello.html', {'name': 'ashwin', 'orders': list(query_set)})
# return render(request, 'hello.html', {'name': 'ashwin', 'result': result})

# def say_hello(request):
#     # Find the contenttype id for the product models for applying tags to the products
#     # content_type = ContentType.objects.get_for_model(Product)
#     # objects is a manager, is a gateway for DB, get_for_model() is a manager method
#     # query_set = TaggedItem.objects \
#     #     .filter(
#     #         content_type=content_type, object_id=1).select_related('tag')
#     query_set = TaggedItem.objects.get_tags_for(Product, 1)
#     return render(request, 'hello.html', {'name': 'ashwin', 'tags': list(query_set)})

# def say_hello(request):
#     '''creating data'''
#     # collection = Collection()
#     # collection.title = 'Video Games'
#     # collection.featured_product = Product(pk=1)
#     # collection.save()  # saving data in DB
#     # # Short Hand
#     # # Collection.objects.create(title='a', featured_product_id=1)

#     '''updating data'''
#     collection = Collection.objects.get(
#         pk=1)  # pk is working as a primary_key along with any name in database
#     collection.title = 'Games'
#     collection.featured_product = None
#     collection.save()  # saving data in DB

#     return render(request, 'hello.html', {'name': 'ashwin'})

@transaction.atomic()  # using decorator we can create a transaction function seperatoly
def say_hello(request):
    # ......... some code here
    #  you want for specific db operation wants to use transaction, context manager
    with transaction.atomic():
        order = Order()
        order.customer__id = 1
        order.save()

    # In relational Databse always create a parent record first before createing chld record
        # above code is parent record and below one is child because of foreign relation

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()
    return render(request, 'hello.html', {'name': 'ashwin'})


'''
 * lets map this view to a URL(uniform resource locator) for seeing the content of that function
 * When we get request of that URL, this function will be called.
'''
