from django.contrib import messages
from django.contrib import admin
from django.utils.translation import ngettext

from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    @admin.action(description='Verifikasi post yang dipilih')
    def make_verify(self, request, queryset):
        updated = queryset.update(verified=True)
        self.message_user(request, ngettext( 
            '%d Post Berhasil Diverfikasi.',
            '%d Posts Berhasil Diverfikasi.',
            updated
        ) % updated, messages.SUCCESS)

    fields = (
        ('title', 'verified'),
        ('author', 'ig_account'),
        'category', 'image', 'content'
    )
    list_display = ('title', 'author', 'verified')
    list_filter = ('verified', 'category')
    list_per_page = 20
    actions = [make_verify]

admin.site.register(Post, PostAdmin)
admin.site.register(Category)