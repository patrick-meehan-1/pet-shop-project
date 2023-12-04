from django.shortcuts import render, redirect
from .models import Cart, CartItem, OrderItem
from .models import Checkout
from shop.models import Product
from django.contrib import messages
from decimal import Decimal
import uuid
from django.shortcuts import get_object_or_404, redirect
from payments import get_payment_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import MyPaymentForm 
from django.contrib.auth.decorators import login_required




@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_item.quantity = 1  # redundacy
    else:
        cart_item.quantity += 1

    cart_item.save()

    messages.success(request, "Product added to cart successfully.")
    return redirect('cart:cart_detail')




@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else []
    total_cost = sum(item.sub_total() for item in cart_items) if cart else 0

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_cost': total_cost,
    }
    return render(request, 'cart_detail.html', context)




@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return redirect('cart:cart_detail')

    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart:cart_detail')


@login_required
def checkout(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()

    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect('cart:cart_detail')

    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        messages.info(request, "Your cart is empty.")
        return redirect('cart:cart_detail')

    cart_total = sum(item.sub_total() for item in cart_items)

    if request.method == "POST":
        payment_form = MyPaymentForm(request.POST)
        if payment_form.is_valid():
            checkout_instance = Checkout(
                user=user,
                shipping_address=payment_form.cleaned_data['shipping_address'],
                payment_method=payment_form.cleaned_data['payment_method'],
                order_total=cart_total
            )
            checkout_instance.save()

            # Create OrderItem instances for each CartItem
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=checkout_instance,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Clear the cart
            cart_items.delete()
            cart.delete()

            return redirect('cart:order_confirmation') 
    else:
        payment_form = MyPaymentForm()

    context = {
        'payment_form': payment_form,
        'cart_total': cart_total,
        'cart_items': cart_items
    }
    return render(request, 'checkout.html', context)



@login_required
def order_confirmation(request):
    
    recent_order = Checkout.objects.filter(user=request.user).order_by('-created_at').first()

  
    recent_cart = Cart.objects.filter(user=request.user).order_by('-date_added').first()

  
    items = CartItem.objects.filter(cart=recent_cart) if recent_cart else []

    context = {
        'order': recent_order,
        'items': items,
        'total_cost': recent_order.order_total if recent_order else None,
    }
    return render(request, 'order_confirmation.html', context)

@login_required
def order_list(request):

    orders = Checkout.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_list.html', {'orders': orders})




from django.shortcuts import get_object_or_404, render

def order_detail(request, order_id):
    # Fetch the order; if it doesn't exist, return a 404 response
    order = get_object_or_404(Checkout, id=order_id, user=request.user)

    # Fetch related OrderItem instances
    order_items = OrderItem.objects.filter(order=order)

    # Render the template with the order and its items
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})





