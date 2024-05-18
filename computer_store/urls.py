from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('log-in', views.log_in, name='log_in'),   
    path('log-out', views.log_out, name='log_out'), 

    #Category
    path('category-create', views.category_create, name='category_create'),
    path('category-update/<int:id>/', views.category_update, name='category_update'),
    path('category-list', views.category_list, name='category_list'),
    path('category-delete/<int:id>/', views.category_delete, name='category_delete'),

    #Product
    path('product-create', views.product_create, name='product_create'),
    path('product-list', views.product_list, name='product_list'),
    path('product-update/<str:code>/', views.product_update, name='product_update'),
    path('product-delete/<str:code>/', views.product_delete, name='product_delete'),

    #EnterProduct
    path('enter-product-create', views.enterproduct_create, name='enterproduct_create'),
    path('enter-product-list', views.enterproduct_list, name='enterproduct_list'),

    #OutProduct
    path('out-product-create', views.outproduct_create, name='outproduct_create'),
    path('out-product-list', views.outproduct_list, name='outproduct_list'),


    #ReturnProduct
    path('return-product-create', views.returnproduct_create, name='returnproduct_create'),
    path('return-product-list', views.returnproduct_list, name='returnproduct_list'),
]