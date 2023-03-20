from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from core.core import get_user_from_request
from core.models import MainUser


# Create your models here.
class Blog(models.Model):
    creation_date = models.DateTimeField('Дата создания', auto_now_add=True)
    author = models.ForeignKey(MainUser, verbose_name='Автор', related_name='blog_author_id', on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='Slug', unique=True, null=True, )
    name = models.CharField('Название', max_length=45)
    text = RichTextUploadingField('Текст')
    main_image = models.ImageField('Главное изобраение новости', upload_to='portal/', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.author = get_user_from_request()
        if not self.slug:
            from django.utils.text import slugify
            from unidecode import unidecode
            import random
            import string
            slug = slugify(unidecode(self.name), allow_unicode=True)
            self.slug = str(Blog.objects.first().pk) + random.choice(string.ascii_letters) + slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Блог'
        ordering =['-creation_date']

class BlogGalery(models.Model):
    blog_id = models.ForeignKey(Blog, verbose_name='Статья блога', related_name='galery_blog_id', on_delete=models.CASCADE)
    picture = models.ImageField('Изображение', upload_to='portal/', blank=False)

    class Meta:
        verbose_name_plural = 'Галерея'
