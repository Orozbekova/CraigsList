from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from applications.normal_account.models import CustomUser
from main import settings

User = get_user_model()

# Create your models here.
class Category(models.Model):
    slug = models.SlugField(max_length=30, primary_key=True,verbose_name='Название')

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.CharField(max_length=25, unique=True, verbose_name='Название')

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name_plural = 'ПодКатегории'
        verbose_name = 'ПодКатегория'



def validators_number_phone(value):
    if not value.isdigit():
        raise forms.ValidationError("Номер телефона должен состоять только из цифр")

class Post(models.Model):
    CHOICES = (
        ('BISH', 'Бишкек'),
        ('K/B', 'Кара-Балта'),
        ('TOK', 'Токмок'),
        ('KANT', 'Кант'),
        ('SOK', 'Сокулук')
    )
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=30, choices=CHOICES)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory,related_name='posts',on_delete=models.CASCADE,blank=True)
    number_phone = models.CharField('Номер телефона', max_length=11, blank=True, validators=[validators_number_phone])
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'

class Image(models.Model):
    image = models.ImageField(upload_to='images', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')


class Review(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='reviews', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='reviews', on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} --> {self.review}'


class Favorite(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True, on_delete=models.CASCADE,related_name='favorites')
    post = models.ForeignKey(Post,null=True,blank=True, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.owner} --> {self.post}'



class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    # owner = models.OneToOneField(User, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')

    def __str__(self):
        return f'{self.owner}--likes-> {self.post}'




class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rating')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')
    rating = models.SmallIntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ])