from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from shop.models import Product, Category, SubCategory, Brand, Review, CartItem
from ..forms import ProductForm, CustomUserCreationForm
from ..utils import get_cart_session_key
from django.shortcuts import resolve_url 
from shop.cart import Cart
from shop.forms import CartAddProductForm




class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        subcategory = self.request.GET.get('subcategory')
        brand = self.request.GET.get('brand')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        min_rating = self.request.GET.get('min_rating')

        if q:
            queryset = queryset.filter(name__icontains=q)
        if category:
            queryset = queryset.filter(category__id=category)
        if subcategory:
            queryset = queryset.filter(subcategory__id=subcategory)
        if brand:
            queryset = queryset.filter(brand__id=brand)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = SubCategory.objects.all()
        context['brands'] = Brand.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        return context


class SubmitReviewView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        fullname = request.POST.get('fullname')
        rating = request.POST.get('rating')
        text = request.POST.get('text')

        if fullname and rating and text:
            Review.objects.create(
                product=product,
                fullname=fullname,
                rating=rating,
                text=text
            )
            messages.success(request, 'Review submitted successfully.')
        else:
            messages.error(request, 'Please fill in all fields.')

        return redirect('product_detail', product_id=product_id)


class AddToCartView(View):
    def get(self, request, product_id):
        session_key = get_cart_session_key(request)
        product = get_object_or_404(Product, pk=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            session_key=session_key,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart_view')


class CartView(View):
    def get(self, request):
        session_key = get_cart_session_key(request)
        cart_items = CartItem.objects.filter(session_key=session_key)
        total = sum(item.subtotal() for item in cart_items)

        return render(request, 'shop/cart.html', {
            'cart_items': cart_items,
            'total': total
        })


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
        return render(request, 'registration/register.html', {'form': form})


from django.urls import reverse

class LoginUserView(View):
    def get(self, request):
        return render(request, 'shop/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.GET.get('next')
        if not next_url or not next_url.startswith('/'):
            next_url = reverse_lazy('shop:product_list')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

        return render(request, 'shop/login.html')

class LogoutUserView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect(reverse_lazy('shop:product_list'))


class AddProductView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'shop/add_product.html'
    success_url = reverse_lazy('product_list')


class UpdateCartView(View):
    def post(self, request, item_id):
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id)

        if action == 'increment':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrement':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()
        elif action == 'delete':
            cart_item.delete()

        return redirect('cart_view')

class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        return redirect('cart:detail')

class CartRemoveView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:detail')

class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'shop/cart_detail.html', {'cart': cart})
