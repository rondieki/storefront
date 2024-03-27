from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



from .models import Customer, Order, Product


class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'

class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16)
    expiry_date = forms.CharField(label='Expiry Date', max_length=10)
    cvv = forms.CharField(label='CVV', max_length=10)

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(label='Your Message', widget=forms.Textarea)

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone'] 
		
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'image']

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    payment_method = forms.ChoiceField(choices= [('mpesa', 'Mpesa')])#[('stripe', 'Credit/Debit Card'), ('paypal', 'PayPal'), ('mpesa', 'Mpesa')])
    note = forms.CharField(max_length=1000, required=False)
