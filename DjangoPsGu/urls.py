"""
Definition of urls for DjangoPsGu.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('links/', views.links, name='links'),
    path('registration/', views.registration, name='registration'),
    path('feedback/', views.feedback, name='feedback'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/',views.blogpost,name='blogpost'),
    path('newpost/',views.newpost,name='newpost'),
    path('videopost/',views.videopost,name='videopost'),
     path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart_view, name='cart'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
     path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
     path('manage_products/', views.manage_products, name='manage_products'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
     path('create_order/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Войти',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()