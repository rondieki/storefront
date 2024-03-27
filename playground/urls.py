from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('about/', views.about, name="about"),

    path('', views.home, name="home"),
    path('', views.index, name="index"),
    path('products/', views.products, name="products"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('update_customer/<str:pk>/', views.update_customer, name="update"),
    path('payment/', views.payment, name="payment"),
    path('success_page/', views.success_page, name="success_page"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    # path('callback/', views.callback, name='callback'),
    path('stk-push-callback/', views.stk_push_callback, name='stk_push_callback'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)