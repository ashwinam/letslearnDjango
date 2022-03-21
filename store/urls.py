from django.urls import path, include
# from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views

# parent routers drf_nested also comes with DefaultRouter & SimpleRouer
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

# child class
product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet,
                        basename='product_reviews')

urlpatterns = [
    # do need to call function we jst pass a reference
    # path('products/', views.product_list),
    # path('products/<int:id>/', views.product_detail),
    # path('collections/', views.collection_list),
    # path('collection/<int:pk>/', views.collection_detail, name='collection-detail'),
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:pk>/', views.ProductDetail.as_view()),
    # path('collections/', views.CollectionList.as_view()),
    # path('collection/<int:pk>/', views.CollectionDetail.as_view(),
    #      name='collection-detail'),
    path('', include(router.urls)),
    path('', include(product_router.urls)),
]
