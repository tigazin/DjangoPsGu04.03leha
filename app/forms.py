"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models import Blog

from .models import CartItem
from .models import Product
from.models import Comment

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'пароль'}))

class FeedbackForm(forms.Form):
    name = forms.CharField(
        label="Ваше имя", 
        min_length=2, 
        max_length=100
    )
    city = forms.CharField(
        label="Ваш город", 
        min_length=2, 
        max_length=100
    )
    product = forms.CharField(
        label="Какой шаблон вы приобрели", 
        min_length=2, 
        max_length=100
    )
    rating = forms.ChoiceField(
        label="Оцените наш сайт", 
        choices=[('1', '1 (плохо)'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5 (отлично)')],
        widget=forms.RadioSelect, 
        initial='5'
    )
    usage = forms.ChoiceField(
        label="Как часто вы используете наши шаблоны", 
        choices=[
            ('1', 'Каждый день'),
            ('2', 'Несколько раз в день'),
            ('3', 'Несколько раз в неделю'),
            ('4', 'Несколько раз в месяц')
        ],
        widget=forms.RadioSelect, 
        initial='1'
    )
    subscribe = forms.BooleanField(
        label="Получать новости и обновления?", 
        required=False
    )
    email = forms.EmailField(
        label="Ваш e-mail", 
        min_length=7
    )
    message = forms.CharField(
        label="Ваш отзыв о нашем сайте", 
        widget=forms.Textarea(attrs={'rows': 12, 'cols': 20})
    )

class CommentForm (forms.ModelForm):

    class Meta:

        model = Comment # используемая модель

        fields = ('text',) # требуется заполнить только поле text

        labels = {'text': "Комментарий"} # метка к полю формы text

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title','description','content','image',)
        labels = {'title':'Заголовок','description':'Краткое содержание','content':'Полное содержание','image':'Картинка'}
        


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']