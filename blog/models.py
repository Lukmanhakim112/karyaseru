import itertools
from urllib.parse import urlparse, parse_qs

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

from PIL import Image
from django_quill.fields import QuillField


class Category(models.Model):
    IMAGE_FORMAT = ['jpeg', 'jpg', 'png', 'svg', 'gif', 'bmp']
    icon = models.FileField('Icon Kategory', upload_to='category_icon/', null=True, validators=[FileExtensionValidator(IMAGE_FORMAT)])
    category = models.CharField('Kategori', max_length=50)
    slug = models.SlugField(null=True, blank=True, help_text="Untuk Slug jangan diisi (otomatis oleh sistem).")

    def _generate_slug(self):
        value = self.category
        slug_candidate = slugify(value, allow_unicode=True)

        # add number to slug, if the slug already exist
        for i in itertools.count(1):
            # pylint: disable=maybe-no-member
            if not Post.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = f'{slug_candidate}-{i}'

        self.slug = slug_candidate

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super(Category, self).save(*args, **kwargs)

class Post(models.Model):
    verified = models.BooleanField('Terverivikasi', default=False)
    title = models.CharField('Judul Post (Karya)', max_length=70, db_index=True)
    author = models.CharField('Penulis', max_length=100)
    slug = models.SlugField()
    category = models.ManyToManyField(Category, verbose_name="Kategori")

    image = models.ImageField('Gambar/Photo')
    video = models.URLField('Link Video', null=True, blank=True, help_text="Masukan link video jika ada, untuk disematkan di artikel.")
    v_yt_id = models.CharField(max_length=30, null=True, blank=True)
    content = QuillField(verbose_name="Konten/Tulisan", null=True)
    ig_account = models.CharField('Link Akun Instagram', max_length=100, help_text='Isi dengan link instagram penulis.')

    updated_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

    def _generate_slug(self):
        value = self.title
        slug_candidate = slugify(value, allow_unicode=True)

        # add number to slug, if the slug already exist
        for i in itertools.count(1):
            # pylint: disable=maybe-no-member
            if not Post.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = f'{slug_candidate}-{i}'

        self.slug = slug_candidate

    def _trim_yoututbe_id(self):
        video_url = self.video
         
        try:
            url_parsed = urlparse(video_url)
            url_parsed = parse_qs(url_parsed.query)
            return url_parsed["v"][0]
        except KeyError:
            # pylint: disable=maybe-no-member
            url = video_url.split("/")
            return url[3]


    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        self.v_yt_id = self._trim_yoututbe_id()

        super(Post, self).save(*args, **kwargs)
        # pylint: disable=maybe-no-member
        img = Image.open(self.image.path)
        if img.height > 450 or img.width > 853:
            output_size = (850,490)
            img.thumbnail(output_size)
            img.save(self.image.path)
