from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Product, Review

class SubmitReviewView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        fullname = request.POST.get('fullname')
        rating = request.POST.get('rating')
        text = request.POST.get('text')

        if not (fullname and rating and text):
            messages.error(request, "All fields are required.")
            return redirect('shop:product_detail', product.id)

        try:
            rating = float(rating)
            if not (0 <= rating <= 5):
                raise ValueError("Rating must be between 0 and 5.")
        except ValueError:
            messages.error(request, "Invalid rating. Must be a number between 0 and 5.")
            return redirect('shop:product_detail', product.id)


        Review.objects.create(
            product=product,
            fullname=fullname,
            rating=rating,
            text=text
        )
        messages.success(request, "Review submitted successfully!")
        return redirect('shop:product_detail', product.id)
