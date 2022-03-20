from django.urls import path
from . import views

urlpatterns = [
    # do need to call function we jst pass a reference
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),
    path('collections/', views.collection_list),
    path('collection/<int:pk>/', views.collection_detail, name='collection-detail'),
]
