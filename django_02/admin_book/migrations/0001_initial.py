# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-11 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bname', models.CharField(db_index=True, help_text='Название книги', max_length=255, unique=True, verbose_name='Название книги')),
                ('brating', models.PositiveSmallIntegerField(db_index=True, default=0)),
                ('bcdateadd', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('bimagesmall', models.ImageField(blank=True, editable=False, upload_to='books_image_small/')),
                ('bimagelarge', models.ImageField(upload_to='books_image_large/', verbose_name='Картинка')),
            ],
        ),
        migrations.CreateModel(
            name='Books_Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baauthor', models.CharField(db_index=True, help_text='Автор книг', max_length=255, unique=True, verbose_name='Имя автора книг')),
            ],
        ),
        migrations.CreateModel(
            name='Books_Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bcname', models.CharField(db_index=True, help_text='Название категории книг.', max_length=255, unique=True, verbose_name='Название категории книг')),
                ('bcdescr', models.TextField(blank=True, help_text='Описание категории книг', verbose_name='Описание категории книг')),
            ],
        ),
        migrations.AddField(
            model_name='books',
            name='bauthor',
            field=models.ForeignKey(help_text='Автор книги', null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_book.Books_Author', verbose_name='Автор книги'),
        ),
        migrations.AddField(
            model_name='books',
            name='bcategories',
            field=models.ManyToManyField(db_index=True, help_text='Категория книги, может быть несколько.', to='admin_book.Books_Categories', verbose_name='Категория книги'),
        ),
    ]
