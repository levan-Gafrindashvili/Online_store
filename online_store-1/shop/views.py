from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category, SubCategory, Brand, Review, CartItem
from .forms import ProductForm
from .utils import get_cart_session_key

# Product list view with filtering
def product_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    brand = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category__id=category)
    if subcategory:
        products = products.filter(subcategory__id=subcategory)
    if brand:
        products = products.filter(brand__id=brand)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if min_rating:
        products = products.filter(rating__gte=min_rating)

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'brands': Brand.objects.all(),
    }
    return render(request, 'shop/product_list.html', context)

# Product detail view
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews
    })

# Submit review
@require_POST
def submit_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviewer_name = request.POST.get('reviewer_name')
    text = request.POST.get('text')

    try:
        rating = int(request.POST.get('rating'))
    except (TypeError, ValueError):
        messages.error(request, "Invalid rating submitted.")
        return redirect('product_detail', pk=product.id)

    Review.objects.create(
        product=product,
        reviewer_name=reviewer_name,
        rating=rating,
        text=text
    )
    return redirect('product_detail', pk=product.id)

# Add product to cart
def add_to_cart(request, product_id):
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

# Cart view
def cart_view(request):
    session_key = get_cart_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.subtotal() for item in cart_items)

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

# Update cart item quantity or delete
@require_POST
def update_cart(request, item_id):
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

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('add_product')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'shop/login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Add product view (staff only)
@login_required
def add_product(request):
    if not request.user.is_staff:  # Optional: restrict to staff only
        return redirect('product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'shop/add_product.html', {'form': form})
