import itertools

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from django_quill.fields import QuillField
from PIL import Image


class Category(models.Model):
    category = models.CharField('Kategori', max_length=50)

    def __str__(self):
        return self.category

class Post(models.Model):
    title = models.CharField('Judul Post (Karya)', max_length=70, db_index=True)
    author = models.CharField('Author', max_length=100)
    slug = models.SlugField()
    category = models.ManyToManyField(Category)

    image = models.ImageField('Gambar/Photo', upload_to='post/images/')
    content = QuillField(null=True)
    ig_account = models.CharField('Akun Instagram', max_length=100, help_text='Isi dengan link instagram author.')

    updated_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

    def _generate_slug(self):
        max_length = self._meta.get_field('slug').max_length
        value = self.title
        slug_candidate = slugify(value, allow_unicode=True)

        # add number to slug, if the slug already exist
        for i in itertools.count(1):
            if not Post.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = f'{slug_candidate}-{i}'

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super(Post, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 450 or img.width > 853:
            output_size = (850,490)
            img.thumbnail(output_size)
            img.save(self.image.path)
