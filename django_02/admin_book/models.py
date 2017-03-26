from django.db import models

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
    bimagesmall = models.ImageField(upload_to='books_image_small/',
                                    blank=True, editable=False)
    bimagelarge = models.ImageField(upload_to='books_image_large/',
                                    blank=False, verbose_name="Картинка")

    def __str__(self):
        return self.bname
