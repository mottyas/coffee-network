# Generated by Django 3.2.9 on 2022-01-07 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='new_field',
            field=models.CharField(blank=True, max_length=100, verbose_name='Какое-то поле'),
        ),
    ]
