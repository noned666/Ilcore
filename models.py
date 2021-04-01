from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse



class Category(models.Model):
        
    name = models.CharField(max_length=64, verbose_name='название')
    slug = models.CharField(max_length=100, unique='title', verbose_name='url')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return (self.name)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Article(models.Model):
    class Meta:
        db_table = "Article"
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
   
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Название статьи', max_length=200)
    full_text = models.TextField('Текст')
    created_date = models.DateTimeField('Дата публикации', default= None)
    image = models.ImageField('Фотография статьи', upload_to='images/', null=True, blank=True)
    
    def __str__(self):
        return self.title



class Comment(models.Model):

    class Meta:
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    email = models.EmailField('Имэйл', max_length=50)
    author = models.CharField('Автор', max_length=200)
    com_text = models.TextField('Текст комментария')
    created_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    active = models.BooleanField(default=True)  

    def __str__(self):
        return self.email




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField('Биография', max_length=500, blank=True)
    location = models.CharField('Город', max_length=30, blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)

    def __str__(self):
        return self.user
   
