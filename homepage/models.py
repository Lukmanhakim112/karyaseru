from django.db import models

from django_quill.fields import QuillField

class Homepage(models.Model):
    slogan = models.CharField('Slogan', max_length=100)
    expl = QuillField(verbose_name='Penjelasan Karyaseru')

    def __str__(self):
        return self.slogan
    