from django.urls import path
from . import views

urlpatterns = [
    # Product listing and detail
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # Submit a review for a product (POST)
    path('product/<int:pk>/review/', views.submit_review, name='submit_review'),

    # Cart views: display, add items, update quantities
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),

    # Authentication views
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Adding new products
    path('add-product/', views.add_product, name='add_product'),
]
