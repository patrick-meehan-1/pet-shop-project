from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Category, Product, Review
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import ReviewForm
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
def prod_list(request, category_id=None):
    category = None
    products = Product.objects.filter(available=True)
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, available=True)
    
    paginator = Paginator(products, 6)
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop/category.html', {'category': category, 'prods': products})

def product_detail(request, category_id, product_id):
    product = get_object_or_404(Product, category_id=category_id, id=product_id)
    return render(request, 'shop/product.html', {'product': product})

class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'shop.add_product'
    model = Product
    fields = ['name', 'description',  'category', 'price', 'image', 'stock', 'available', 'pet']
    template_name = 'shop/new_product.html'

def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        author = request.user
        review = form.cleaned_data['review']
        reviewObject = Review(product=product, review=review, author=author)
        reviewObject.save()

        return redirect('shop:all_products')

        
    
    form = ReviewForm()
    context = {
        "product": product,
        "form": form
    }
    return render(request, 'new_review.html', context)