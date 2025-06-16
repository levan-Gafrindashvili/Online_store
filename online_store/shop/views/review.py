from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Product, Review

class SubmitReviewView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        fullname = request.POST.get('fullname')
        rating = request.POST.get('rating')
        text = request.POST.get('text')

        if fullname and rating and text:
            Review.objects.create(
                product=product,
                fullname=fullname,
                rating=float(rating),
                text=text
            )

        return redirect(reverse('shop:product_detail', args=[product.id]))
