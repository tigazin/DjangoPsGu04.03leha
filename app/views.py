"""
Definition of views.
"""

from datetime import datetime
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpRequest
from .forms import FeedbackForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Comment # использование модели комментариев
from django.contrib.auth.decorators import user_passes_test
from .forms import CommentForm # использование формы ввода комментария
from .forms import BlogForm # использование формы ввода комментария
from .models import Product, Cart, CartItem
from .forms import AddToCartForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Product, Cart, CartItem
from .forms import AddToCartForm, BlogForm, FeedbackForm, CommentForm,ProductForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.admin.forms import AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Cart, Order

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def blog(request):
    posts = Blog.objects.all()

    assert isinstance(request,HttpRequest)
    return render(
        request,
        'app/blog.html',{
        'title':'Блог',
        'posts':posts,
        'year':datetime.now().year,
        })

def blogpost(request,parametr):
    assert isinstance(request,HttpRequest)
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST": # после отправки данных формы на сервер методом POST

        form = CommentForm(request.POST)

        if form.is_valid():

            comment_f = form.save(commit=False)

            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя

            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату

            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий

            comment_f.save() # сохраняем изменения после добавления полей

        return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария

    else:

        form = CommentForm() # создание формы для ввода комментария
    return render(
        request,
        'app/blogpost.html',{
            'post_1':post_1,
            'year':datetime.now().year,
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы

            'form': form, 
            }
        )
def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Тут контакты',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Тут о нас',
            'year':datetime.now().year,
        }
    )
def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {

        }
    )
def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {

        }
    )
def feedback(request):
    assert isinstance(request, HttpRequest)
    data = None

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'city': form.cleaned_data['city'],
                'product': form.cleaned_data['product'],
                'rating': form.cleaned_data['rating'],
                'usage': form.cleaned_data['usage'],
                'subscribe': 'Да' if form.cleaned_data['subscribe'] else 'Нет',
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            form = None
        else:
            data = None
    else:
        form = FeedbackForm()

    return render(
        request,
        'app/feedback.html',
        {
            'form': form,
            'data': data,
        }
    )
def newpost(request):

    if request.method == 'POST':
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()
            return redirect('blog')
    else:
        blogform = BlogForm()
    
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',
            'year': datetime.now().year,
        }
    )
def registration(request):
    if request.method =="POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()

            regform.save()

            return redirect('home')
    else:
         regform = UserCreationForm()
    assert isinstance(request,HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform':regform,
            'year':datetime.now().year,
        }
        )
    
def product_list(request):
    products = Product.objects.all()
    return render(request, 'app/product_list.html', {'products': products})

def initialize_cart(request):
    if not request.session.session_key:
        request.session.create()
    if 'cart' not in request.session:
        request.session['cart'] = {}

def product_list(request):
    initialize_cart(request)
    products = Product.objects.all()
    return render(request, 'app/product_list.html', {'products': products})
@login_required
def cart_view(request):
    initialize_cart(request)
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()  # Получаем все товары в корзине
    total = sum(item.product.price * item.quantity for item in items)  # Считаем общую стоимость

    return render(request, 'app/cart.html', {'cart': items, 'total': total})
@login_required
@login_required
def add_to_cart(request, product_id):
    initialize_cart(request)
    cart = Cart.objects.get(user=request.user)  # Получаем корзину пользователя
    product = get_object_or_404(Product, id=product_id)  # Получаем товар

    # Проверяем, есть ли уже этот товар в корзине
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:  # Если товар уже есть в корзине, увеличиваем его количество
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)

    # Удаляем товар из корзины
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()

    return redirect('cart')

def clear_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart.cartitem_set.all().delete()
    return redirect('cart')

def checkout(request):
    return render(request, 'app/checkout.html', {})
# Увеличение количества товара
def increase_quantity(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def decrease_quantity(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def is_manager(user):
    return user.groups.filter(name='manager').exists()

@user_passes_test(is_manager)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'app/add_product.html', {'form': form})

def is_manager_or_admin(user):
    return user.is_superuser or user.is_staff or user.groups.filter(name='manager').exists()
@login_required
@user_passes_test(is_manager_or_admin)

def manage_products(request):
    if request.method == 'POST':
        if 'add_product' in request.POST:  # Добавление товара
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('manage_products')

        elif 'delete_product' in request.POST:  # Удаление товара
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            return redirect('manage_products')

    # Отображение страницы
    form = ProductForm()
    products = Product.objects.all()
    return render(request, 'app/manage_products.html', {'form': form, 'products': products})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)  # Только админы и суперпользователи
def manage_users(request):
    users = User.objects.all()

    if request.method == 'POST':
        # Добавление нового пользователя
        if 'add_user' in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage_users')

        # Удаление пользователя
        elif 'delete_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return redirect('manage_users')

        # Изменение пользователя (форма будет в отдельной странице или модальном окне)

    else:
        form = UserCreationForm()

    return render(request, 'app/manage_users.html', {'users': users, 'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserChangeForm(instance=user)

    return render(request, 'app/edit_user.html', {'form': form, 'user': user})
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)  # Доступ только админам и суперпользователям
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Получение пользователя по ID

    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')  # Возврат к странице управления пользователями
    else:
        form = UserChangeForm(instance=user)

    return render(request, 'app/edit_user.html', {'form': form, 'user': user})

def some_view(request):
    is_manager_or_admin = (
        request.user.is_authenticated and
        request.user.groups.filter(name__in=["manager", "admin"]).exists()
    )
    return render(request, 'template.html', {
        'is_manager_or_admin': is_manager_or_admin,
    })
def some_view_admin(request):
    is_manager_or_admin = (
        request.user.is_authenticated and
        request.user.groups.filter(name__in=["admin"]).exists()
    )
    return render(request, 'template.html', {
        'is_manager_or_admin': is_admin,
    })

@login_required
def create_order(request):
    cart = Cart.objects.get(user=request.user)
    
    if request.method == 'POST':
        cart_items = cart.cartitem_set.all()  # Получаем все товары в корзине
        if cart_items.count() == 0:
            return redirect('cart')  # Если корзина пуста, возвращаем в корзину
        
        # Создаём новый заказ для текущей корзины
        order = Order.objects.create(user=request.user, cart=cart, order_type='in_progress')

        # Не очищаем корзину, чтобы пользователь мог продолжать добавлять товары
        return redirect('order_detail', order_id=order.id)  # Перенаправляем на страницу с деталями заказа

    return redirect('cart')  # Если GET-запрос, перенаправляем в корзину

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'app/order_detail.html', {'order': order})

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def manage_orders(request):
    orders = Order.objects.all()

    if request.method == 'POST':
        if 'delete_order' in request.POST:
            order_id = request.POST.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            order.delete()
            return redirect('manage_orders')

        elif 'mark_completed' in request.POST:  # Закрыть заказ
            order_id = request.POST.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            order.order_type = 'completed'
            order.save()
            return redirect('manage_orders')

    return render(request, 'app/manage_orders.html', {'orders': orders})


