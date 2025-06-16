from django.urls import path
from shop.views.cart import CartAddView, CartRemoveView, CartDetailView

app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='detail'),
    path('add/<int:product_id>/', CartAddView.as_view(), name='add'),
    path('remove/<int:product_id>/', CartRemoveView.as_view(), name='remove'),
]
