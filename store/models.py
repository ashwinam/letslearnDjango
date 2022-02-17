from django.db import models


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Product(models.Model):
    # Django Creates ID field automatically, if you want to set own
    # sku = models.CharField(max_length=255, primary_key=True) # creates a ID
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    '''
    what is slug field?
    we see in websites where we ask something in website so it gives us a id and a question that we asked in with hyphens but in page it gives us the normal questions with better spacing but in address spot we see the hyphen
     like google.com/544351/what-is-slug-field, so what-is-slug-field in adress bar is a slug it means it contains only numbers, letters, underscores and hyphen'-', anyother character is replaced,
     the whole point of adding slug is to make easier for search engines to find the content its useful for SEO(search engine optimization)Techniques.
    '''
    description = models.TextField()  # doesn't have any required arguments
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)  # 9999.99
    inventory = models.IntegerField()
    # auto_now automatically set current date when we update the product
    last_update = models.DateTimeField(auto_now=True)
    # protect it helps to not delete the collection
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    # Django automatically set reverse relationships
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'  # upper letter indicates the const variable, dont mess here
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICE = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICE, default=MEMBERSHIP_BRONZE)

    class Meta:
        db_table = 'store_customers'
        indexes = [
            models.Index(fields=['last_name', 'first_name'])
        ]


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICE = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    # auto_now_add set first time current date.
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICE, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrederItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.IntegerField(null=True)
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
