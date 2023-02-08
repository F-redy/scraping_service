from django.db import models
from django.utils.text import slugify


class City(models.Model):
    name = models.CharField('Название населенного пункта', max_length=100, unique=True)
    slug = models.SlugField('url', max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Название населенного пункта'
        verbose_name_plural = 'Название населенных пунктов'
