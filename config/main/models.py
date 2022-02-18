from time import time

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from pytils.translit import slugify


def gen_slug(q):
    """Генератор слагов от времени"""
    new_slug = slugify(q)
    return new_slug + '-' + str(int(time()))


class News(models.Model):
    """Модель для статей(новостей)"""
    title = models.CharField(max_length=250, verbose_name='Наименование')
    slug = models.SlugField(max_length=250, db_index=True, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               max_length=100, blank=True, null=True, verbose_name='Имя автора')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория',
                                 related_name='news')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    tags = models.ManyToManyField('Tag', blank=True, related_name='news')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(models.Model):
    """Модель для категорий"""
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категорий')
    slug = models.SlugField(max_length=150, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Модель для тэгов"""
    title = models.CharField(max_length=50, db_index=True, verbose_name='Имя тэга')
    slug = models.SlugField(max_length=50, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


