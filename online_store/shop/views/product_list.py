from django.views.generic import ListView
from shop.models import Product, Category, SubCategory, Brand
from django.db.models import Avg

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all().annotate(avg_rating=Avg('reviews__rating'))
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
            try:
                min_rating_val = float(min_rating)
                queryset = queryset.filter(avg_rating__gte=min_rating_val)
            except ValueError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = SubCategory.objects.all()
        context['brands'] = Brand.objects.all()
        return context
