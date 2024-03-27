from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.sessions.models import Session
from django.utils import timezone
import pkg_resources
import stripe
from django.urls import reverse


# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, PaymentForm
from .filters import OrderFilter

from .models import Product, Cart, Order, OrderLine


stripe.api_key = settings.STRIPE_SECRET_KEY


from .forms import ProductForm


def index(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the index page after successful form submission
    else:
        form = ProductForm()
    return render(request, 'index.html', {'form': form})


@login_required(login_url='login')
def payment(request):
    payment_form = PaymentForm(request.POST or None)
    if request.method == 'POST' and payment_form.is_valid():
        # Process the payment
        # Redirect or display a success message
        pass
    
    return render(request, 'payment.html', {'payment_form': payment_form})

def success_page(request):
    return render(request, 'success_page.html')

	
def process_payment(request):
    # Process payment logic here
    # Redirect to success page upon successful payment
    return redirect(reverse('success_page'))


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def home(request):
    categories = {
        "Electronics": ["Product 1", "Product 2", "Product 3"],
        "Fashion": ["Product 4", "Product 5", "Product 6"],
        # Add more categories and products as needed
    }
    return render(request, 'index.html', {'categories': categories})

def customer(request, pk):
    customer = Customer.objects.get(pk=pk)
    orders = Order.objects.filter(customer=customer)
    order_count = orders.count()
    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
    }
    return render(request, 'customer.html', context)


def calculate_total_price(cart_items):
    # Placeholder function to calculate total price
    total_price = 0
    for item in cart_items:
        total_price += item.price  # Assuming each item has a price attribute
    return total_price

def cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    products = cart.products.all()

    # Calculate total price
    total_price = sum(product.price for product in products)

    context = {
        'products': products,
        'total_price': total_price,
        'total_items': products.count(),  # Count total items in the cart
    }

    return render(request, 'cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.user.is_authenticated:
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Check if the product is already in the cart
        cart_product, cart_product_created = cart.products.through.objects.get_or_create(cart=cart, product=product)
        
        if hasattr(cart_product, 'quantity'):
            # If the cart_product object has a 'quantity' attribute, increase the quantity
            cart_product.quantity += 1
            cart_product.save()
        else:
            # If the cart_product object doesn't have a 'quantity' attribute, add it with quantity 1
            cart.products.add(product, through_defaults={'quantity': 1})
        
        return redirect('cart')  # Assuming you have a URL named 'cart' for the cart page
    else:
        # Handle case where user is not authenticated
        return redirect('login')  # Redirect user to login page or show a message

def view_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = cart.products.all()
    return render(request, 'cart.html', {'cart_items': cart_items})


def calculate_total_price(cart_items):
    total_price = 0
    for item in cart_items:
        total_price += item.price  # Assuming each item has a 'price' attribute
    return total_price

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'index.html', context)

@login_required(login_url='login')
def products(request):
	products = Product.objects.all()

	return render(request, 'products.html', {'products':products})

@login_required(login_url='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs 

    context = {'customer':customer, 'orders':orders, 'order_count':order_count,
    'myFilter':myFilter}
    return render(request, 'customer.html',context)


@login_required(login_url='login')
def update_customer(request, pk):
    customer = Customer.objects.get(pk=pk)
    form = Customer(instance=customer)
    if request.method == 'POST':
        form = Customer(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/', pk=pk)  # Redirect to customer  page
    return render(request, 'update.html', {'form': form, 'customer': customer})

@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
    customer = Customer.objects.get(pk=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('payment'))

    context = {'form':formset}
    return render(request, 'order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'delete.html', context)

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart.products.remove(product)  # Remove the product from the cart
        return redirect('cart')
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def checkout(request):
    if request.method == 'POST':
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Fetch cart items
        cart_items = cart.products.all()
        # print(cart_items)
        # Calculate total price and total items
        total_price = sum(item.price for item in cart_items)
        # total_items = len(cart_items)

        # Create order
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            # total_items=total_items,
            payment_status='Pending',
            status='New',
            note=None,
        )

        # Move cart items to order lines
        for item in cart_items:
            OrderLine.objects.create(
                order=order,
                product=item.name,
                # quantity=item.quantity,  # Assuming each product has a quantity of 1 in the cart
                price=item.price  # Assuming each product has a 'price' field
            )

        # Clear the cart
        cart.products.clear()

        return redirect('payment')  # Redirect to order confirmation page
    else:
        return HttpResponseNotAllowed(['POST'])
