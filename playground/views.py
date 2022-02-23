from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from store.models import Product


# pull data from db
# Trandform Data
# send emails and so on.


def say_hello(request):
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
    query_set = Product.objects.filter(inventory=F('collection_id'))
    return render(request, 'hello.html', {'name': 'ashwin', 'products': list(query_set)})
    # so for dynamic content we pass a dictionery as a third parameter


'''
 * lets map this view to a URL(uniform resource locator) for seeing the content of that function
 * When we get request of that URL, this function will be called.
'''
