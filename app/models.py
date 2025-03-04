"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from datetime import datetime 
from django.urls import reverse
from django.contrib.auth.models import User

class Blog(models.Model):

    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")

    description = models.TextField(verbose_name = "Краткое содержание")

    content = models.TextField(verbose_name = "Полное содержание")

    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")

    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default = 'temp.jpg',verbose_name = 'Путь к картинке')

# Методы класса:

def get_absolute_url(self): # метод возвращает строку с URL-адресом записи

    return reverse("blogpost", args=[str(self.id)])

def __str__(self): # метод возвращает название, используемое для представления отдельных записей в административном разделе

    return self.title

# Метаданные – вложенный класс, который задает дополнительные параметры модели:

class Meta:

    db_table = "Posts" # имя таблицы для модели

    ordering = ["-posted"] # порядок сортировки данных в модели ("-" означает по убыванию)

    verbose_name = "статья блога" # имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)

    verbose_name_plural = "статьи блога" # тоже для всех статей блога

admin.site.register(Blog)
class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Дата комментария")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья комментария")
   

    # Методы класса:
    def __str__(self):  # метод возвращает название, используемое для представления отдельных записей в административном разделе
        return 'Комментарий %d из %s к %s' % (self.id, self.author, self.post)

    # Метаданные — вложенный класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарий к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.FileField(upload_to='products/', verbose_name="Файл изображения товара")

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    products = models.ManyToManyField(Product, through='CartItem', verbose_name="Товары")

    def clear(self):
        self.cartitem_set.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
admin.site.register(Comment)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
# Create your models here.

class Order(models.Model):
    ORDER_TYPE_CHOICES = (
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Изменяем на ForeignKey
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)