from django.db import models
from os import path
from PIL import Image
# Create your models here.

class Books_Categories(models.Model):
    bcname = models.CharField(max_length=255, blank=False, db_index=True,
                              unique=True,
                              help_text='Название категории книг.',
                              verbose_name="Название категории книг")
    bcdescr = models.TextField(blank=True, help_text='Описание категории книг',
                               verbose_name="Описание категории книг")

    def __str__(self):
        return self.bcname


class Books_Author(models.Model):
    baauthor = models.CharField(max_length=255, blank=False, db_index=True,
                                unique=True, help_text='Автор книг',
                                verbose_name="Имя автора книг")

    def __str__(self):
        return self.baauthor


class Books(models.Model):
    bname = models.CharField(max_length=255, blank=False, db_index=True,
                             unique=True, help_text='Название книги',
                             verbose_name="Название книги")
    # для упрощения учебного проекта в связи с ограниченностью времени решил
    # предусмотреть только одного автора для каждой книги.
    bauthor = models.ForeignKey(Books_Author, on_delete=models.SET_NULL,
                                db_index=True, null=True,
                                help_text='Автор книги', blank=False,
                                verbose_name="Автор книги")
    bcategories = models.ManyToManyField(Books_Categories, db_index=True,
                                         help_text='Категория книги, может'
                                                   ' быть несколько.',
                                         verbose_name="Категория книги")
    brating = models.PositiveSmallIntegerField(db_index=True, default=0)
    # Дата автоматически добавится при создании:
    bcdateadd = models.DateTimeField(auto_now_add=True,
                                     verbose_name="Дата добавления")
    bimage = models.ImageField(upload_to='books_image_large/',
                                    blank=False, verbose_name="Картинка")

    def __str__(self):
        return self.bname

    def save(self, *args, **kwargs):
        # Максимальный размер изображения по большей стороне
        _MAX_SIZE = 150
        # Сначала - обычное сохранение
        super(Books, self).save(*args, **kwargs)

        if self.bimage:  # Если картинка есть, то:
            filepath = self.bimage.path
            width = self.bimage.width
            height = self.bimage.height
            max_size = max(width, height)

            # Может, и не надо ничего менять?
            if max_size > _MAX_SIZE:
                image = Image.open(filepath)
                # resize - безопасная функция, она создаёт новый объект, а не
                # вносит изменения в исходный, поэтому так
                image = image.resize(
                    (
                    round(width / max_size * _MAX_SIZE),  # Сохраняем пропорции
                    round(height / max_size * _MAX_SIZE)),
                    Image.ANTIALIAS
                )
                # И не забыть сохраниться
                path_file, file = path.split(filepath)
                file, ext = path.splitext(file)
                filepath = '{}_small{}'.format(path.join(path_file, file), ext)
                image.save(filepath)

    def bimagesmall(self):
        try:
            file = str(self.bimage)
            path_file, file = path.split(file)
            file, ext = path.splitext(file)
            return '{}_small{}'.format(path.join(path_file, file), ext)
        except:
            pass
