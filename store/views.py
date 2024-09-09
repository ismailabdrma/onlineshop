from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
import json
import datetime
from .models import Product, Order, OrderItem, ShippingAddress
from .utils import cartData, guestOrder
from .cart import Cart

# Helper function to avoid repetition
def get_cart_context(request):
    data = cartData(request)
    return {
        'cartItems': data['cartItems'],
        'order': data['order'],
        'items': data['items']
    }

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def store(request):
    context = get_cart_context(request)
    context['products'] = Product.objects.all()
    return render(request, 'store/store.html', context)

def cart_view(request):
    context = get_cart_context(request)
    return render(request, 'store/cart.html', context)

def update_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Expect JSON body
            product_id = data['productId']
            action = data['action']
            product = get_object_or_404(Product, id=product_id)
            cart = Cart(request)

            if action == 'add':
                cart.add(product)
            elif action == 'remove':
                cart.remove(product)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=400)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    try:
        customer = request.user.store_customer
        product = get_object_or_404(Product, id=productId)
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, _ = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse('Item was updated', safe=False)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

def checkout(request):
    context = get_cart_context(request)
    return render(request, 'store/checkout.html', context)

@transaction.atomic
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.store_customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    # Create shipping address
    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode']
    )

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total()):
        order.complete = True
    order.save()  # Save the order status

    return JsonResponse("Payment complete", safe=False)