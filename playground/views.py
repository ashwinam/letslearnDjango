from django.shortcuts import render
from django.http import HttpResponse

# pull data from db
# Trandform Data
# send emails and so on.


def calculate():
    x = 1
    return x


def say_hello(request):
    # here it takes request object
    # return HttpResponse('hello World')
    x = calculate()
    return render(request, 'hello.html', {'name': 'ashwin'})
    # so for dynamic content we pass a dictionery as a third parameter


'''
 * lets map this view to a URL(uniform resource locator) for seeing the content of that function
 * When we get request of that URL, this function will be called.
'''
