from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Publication(models.Model):
    title = models.CharField('Название', max_length=50)
    full_text = models.TextField('Текст публикации')
    date = models.DateTimeField('Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    post_image = models.ImageField('Изображение поста', blank=True, upload_to='images/post/')
    post_image_url = models.ImageField('URL изображения поста', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
