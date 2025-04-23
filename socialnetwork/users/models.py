from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    GENDER_CHOICE = (
        ("M", "М"),
        ("F", "Ж"),
        (None, "-"))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField('Аватар пользователя', blank=True, upload_to='images/avatar/')
    avatar_url = models.ImageField('URL аватара пользователя', blank=True)

    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICE, blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)

    status = models.CharField('Статус', max_length=100, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    users_friend = models.ForeignKey(User, related_name='users_friend', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
