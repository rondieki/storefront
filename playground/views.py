from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Sum

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.sessions.models import Session
from django.utils import timezone
import pkg_resources
import stripe
import csv
from django.urls import reverse
from django.db import connection


# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, PaymentForm, CheckoutForm, ContactForm
from .filters import OrderFilter

from .models import Product, Cart, Order, OrderLine, Customer


stripe.api_key = settings.STRIPE_SECRET_KEY


from .forms import ProductForm

from django_daraja.mpesa.core import MpesaClient

def index(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the index page after successful form submission
    else:
        form = ProductForm()
    return render(request, 'index.html', {'form': form})

class DownloadUserReport(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Customer ID', 'Name', 'Phone', 'Email', 'Date Created'])
        customers = Customer.objects.all()
        for customer in customers:
            writer.writerow([customer.id, customer.name, customer.phone, customer.email, customer.date_created])

        return response



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

def thank_you(request):
    return render(request, 'thank_you.html')

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            # For now, let's just print the form data
            return render(request, 'thank_you.html')
            # You can add your logic here to save the data to the database or send an email
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})

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
    orders = customer.order_set.all()
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

@login_required
def cart(request):
    user = request.user
    # Get the Cart object
    cart, created = Cart.objects.get_or_create(user=user)

    # Execute the SQL query to fetch cart items along with their quantities
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.name, cp.quantity, p.price, cp.product_id, p.image
            FROM playground_cart_products AS cp
            INNER JOIN playground_product AS p ON cp.product_id = p.id
            WHERE cp.cart_id = %s
        """, [cart.id])
        cart_items = cursor.fetchall()

        # Fetch all products associated with the cart
        products = cart.products.all()

    # Now cart_items and products contain the fetched data

    # Initialize a list to hold matching products and their details
    matching_products = []

    # Iterate over cart_items and match products with their quantities
    for cart_item in cart_items:
        for product in products:
            if cart_item[3] == product.id:  # Check if product IDs match
                matching_product = {
                    'id': product.id,
                    'name': product.name,
                    'quantity': cart_item[1],  # Quantity from cart_items
                    'price': product.price,
                    'image': product.image.url  # Assuming 'image' is a FileField/ImageField
                }
                matching_products.append(matching_product)
                break  # Break the inner loop once a match is found

    # Now matching_products contains dictionaries with product details

    # Calculate total price and total items
    total_price = sum(item['price'] * item['quantity'] for item in matching_products)
    total_items = sum(item['quantity'] for item in matching_products)

    # Calculate total orders, delivered orders, and pending orders
    total_orders = Order.objects.all().count()
    delivered = Order.objects.filter(status='Delivered').count()
    pending = Order.objects.filter(status='Pending').count()

    # Render the template with the necessary context
    return render(request, 'cart.html', {
        'matching_products': matching_products,
        'total_price': total_price,
        'total_items': total_items,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.user.is_authenticated:
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)

        # Check if the product is already in the cart
        if product in cart.products.all():
            # If the product is already in the cart, increment the quantity
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE playground_cart_products
                    SET quantity = quantity + 1
                    WHERE cart_id = %s AND product_id = %s
                """, [cart.id, product_id])
        else:
            # If the product is not in the cart, add it with quantity 1
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO playground_cart_products (cart_id, product_id, quantity)
                    VALUES (%s, %s, 1)
                """, [cart.id, product_id])
        
        return redirect('cart')  # Redirect to the cart page
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

# @login_required(login_url='login')
def products(request):
	products = Product.objects.all()

	return render(request, 'products.html', {'products':products})

@login_required(login_url='login')
def customer(request, pk_test):
    user = request.user	
    customer = Customer.objects.get(id=pk_test)
    orders = Order.objects.all()
    
    orders = orders.filter(user=user)
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
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)

    # Fetch cart items along with product details using a raw SQL query
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.name, cp.quantity, p.price, cp.product_id
            FROM playground_cart_products AS cp
            INNER JOIN playground_product AS p ON cp.product_id = p.id
            INNER JOIN playground_cart AS c ON cp.cart_id = c.id
            WHERE cp.cart_id = %s
        """, [cart.id])
        cart_items = cursor.fetchall()

    total_price = sum(item[2] * item[1] for item in cart_items)

    print(cart_items)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Extract billing details from the form
            phone_number = form.cleaned_data['phone']
            
            # Initiate STK push
            cl = MpesaClient()
            account_reference = 'reference'
            transaction_desc = 'Description'
            callback_url = 'https://2d84-102-213-93-18.ngrok-free.app/stk_push_callback'
            response = cl.stk_push(phone_number, int(total_price), account_reference, transaction_desc, callback_url)
          
            # Assuming STK push was successful, proceed with order creation
            if response.status_code == 200:
                # Create the order
                order = Order.objects.create(
                    user=user,
                    total_price=total_price,
                    payment_status='Pending',
                    status='pending',  # Assuming the initial status is 'Pending'
                    note=form.cleaned_data.get('note', '')  # Use get() to avoid KeyError
                )

                # Move cart items to order lines
                for item in cart_items:
                    product = Product.objects.get(pk=item[3])  # Get the corresponding product
                    OrderLine.objects.create(
                        order=order,
                        product=product,  # Product name from cart_items
                        quantity=item[1],       # Quantity from cart_items
                        price=item[2] * item[1]  # Price per quantity from cart_items
                    )

                # Empty the cart
                cart.products.clear()

                # Redirect to a success page or payment gateway
                return redirect('success_page')
            else:
                # Handle STK push failure (e.g., display error message)
                return HttpResponse('STK push failed, please try again')

    else:
        form = CheckoutForm()

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    }

    return render(request, 'checkout.html', context)

def stk_push_callback(request):
        data = request.body
        
        return HttpResponse("STK Push in Django👋")
