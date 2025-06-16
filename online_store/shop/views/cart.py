from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from shop.models import Product


class CartAddView(View):
    def post(self, request, product_id):
        get_object_or_404(Product, id=product_id)

        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1

        request.session['cart'] = cart
        request.session.modified = True
        return redirect('shop:cart_detail')


class CartRemoveView(View):
    def post(self, request, product_id):
        cart = request.session.get('cart', {})
        cart.pop(str(product_id), None)

        request.session['cart'] = cart
        request.session.modified = True
        return redirect('shop:cart_detail')


class CartDetailView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        cart_items = []
        total = 0

        for pid, qty in cart.items():
            try:
                product = Product.objects.get(id=pid)
                subtotal = product.price * qty
                cart_items.append({
                    'product': product,
                    'quantity': qty,
                    'subtotal': subtotal
                })
                total += subtotal
            except Product.DoesNotExist:
                continue

        return render(request, 'cart/detail.html', {
            'cart_items': cart_items,
            'total': total,
        })


class UpdateCartView(View):
    def post(self, request, product_id):
        action = request.POST.get('action')
        cart = request.session.get('cart', {})
        pid = str(product_id)

        if action == 'increment':
            cart[pid] = cart.get(pid, 0) + 1

        elif action == 'decrement':
            if pid in cart:
                cart[pid] = cart[pid] - 1
                if cart[pid] <= 0:
                    cart.pop(pid)

        elif action == 'delete':
            cart.pop(pid, None)

        request.session['cart'] = cart
        request.session.modified = True
        return redirect('shop:cart_detail')
