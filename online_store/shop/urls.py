from django.urls import path, include
from .views import (
    ProductListView,
    ProductDetailView,
    SubmitReviewView,
    RegisterView,
    LoginUserView,
    LogoutUserView,
    AddProductView,
    CheckoutView,
    CheckoutSuccessView
)
from shop.views.cart import (
    CartAddView,
    CartRemoveView,
    CartDetailView,
    UpdateCartView,
)

app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:product_id>/review/', SubmitReviewView.as_view(), name='submit_review'),
    path('add-product/', AddProductView.as_view(), name='add_product'),

    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutUserView.as_view(), name='logout'),

    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:product_id>/', CartAddView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:product_id>/', CartRemoveView.as_view(), name='cart_remove'),
    path('cart/update/<int:product_id>/', UpdateCartView.as_view(), name='update_cart'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout/success/', CheckoutSuccessView.as_view(), name='checkout_success'),

]
