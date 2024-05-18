from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('log-in', views.log_in, name='log_in'),   
    path('log-out', views.log_out, name='log_out'), 

    #Category
    path('category-create', views.category_create, name='category_create'),
    path('category-update/<str:code>', views.category_update, name='category_update'),
    path('category-list', views.category_list, name='category_list'),
    path('category-delete/<str:code>', views.category_delete, name='category_delete'),

    #Product
    path('product-create', views.product_create, name='product_create'),
    path('product-list', views.product_list, name='product_list'),
    path('product-update/<str:code>', views.product_update, name='product_update'),
    path('product-delete/<str:code>', views.product_delete, name='product_delete'),

    #EnterProduct
    path('enter-product-create', views.enter_product_create, name='enter_product_create'),
    path('enter-product-list', views.enter_product_list, name='enter_product_list'),

    #OutProduct
    path('out-product-create', views.out_product_create, name='out_product_create'),
    path('out-product-list', views.out_product_list, name='out_product_list'),


    #ReturnProduct
    path('return-product-create', views.return_product_create, name='return_product_create'),
    path('return-product-list', views.return_product_list, name='return_product_list'),
]