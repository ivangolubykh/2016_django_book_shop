from django.db import models
from os import path
from PIL import Image
from django.core.files.storage import default_storage
# Create your models here.


def small_image_faile_name(filepath):
    path_file, file = path.split(filepath)
    file, ext = path.splitext(file)
    return '{}_small{}'.format(path.join(path_file, file), ext)


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

    def bimagesmall(self):
        try:
            return small_image_faile_name(str(self.bimage))
        except:
            pass

    def __str__(self):
        return self.bname

    def save(self, *args, **kwargs):
        # Максимальный размер изображения по большей стороне
        _MAX_SIZE = 150
        # Проверяю, есть ли в БД уже этот объект (радактируем старое или
        # создаём новое?):
        old_obj = False
        try:
            old_obj = Books.objects.get(pk=self.pk)
        except Exception:
            pass
        # Сначала - обычное сохранение
        super(Books, self).save(*args, **kwargs)
        if old_obj and old_obj.bimage.path != self.bimage.path:
            storage, filepath = old_obj.bimage.storage, old_obj.bimage.path
            storage.delete(filepath)
            default_storage.delete(small_image_faile_name(filepath))
        # Если добавиласть новая картинка или изменилась старая, то создаю
        # уменьшенную копию:
        if not old_obj or (old_obj and
                           old_obj.bimage.path != self.bimage.path):
            filepath = self.bimage.path
            width = self.bimage.width
            height = self.bimage.height
            max_size = max(width, height)
            image = Image.open(filepath)
            # Может, и не надо ничего менять?
            if max_size > _MAX_SIZE:
                # resize - безопасная функция, она создаёт новый объект, а не
                # вносит изменения в исходный, поэтому так
                image = image.resize((round(width / max_size * _MAX_SIZE),
                                      round(height / max_size * _MAX_SIZE)),
                                     Image.ANTIALIAS
                                     )
            # И не забыть сохраниться
            filepath = small_image_faile_name(filepath)
            image.save(filepath)

    def delete(self, *args, **kwargs):
        # До удаления записи получаем необходимую информацию
        storage, filepath = self.bimage.storage, self.bimage.path
        # Удаляем сначала модель ( объект )
        super(Books, self).delete(*args, **kwargs)
        # Потом удаляем сам файл
        storage.delete(filepath)
        # Потом удалю созданный мной маленький файл:
        filepath = small_image_faile_name(filepath)
        storage.delete(filepath)
