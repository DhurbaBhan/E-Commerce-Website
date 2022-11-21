from django.urls import path
from shop_app import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('',views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('showcart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address.as_view(), name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('topwears/<slug:data>', views.fashion, name='topwears'),
    path('bottomwears/<slug:data>', views.fashion, name='bottomwears'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name="app/login.html",authentication_form=LoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
]
