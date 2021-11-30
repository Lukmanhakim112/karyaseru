from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Row,  
    Div, Field, HTML
)

from .models import Post, Category


class AuthorForm(forms.Form):
    full_name = forms.CharField(label="Nama Lengkap")
    ig_account = forms.CharField(
        label="Username Instagram", max_length=100,
        help_text="Masukan username instagram kalian (tanpa @)"
    )

class AuthorFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.layout = Layout(
            Row(
                Div(Field('full_name', css_class="form-control-sm"), css_class='col-12 col-sm-6'),
                Div(Field('ig_account', css_class="form-control-sm"), css_class='col-12 col-sm-6'),
                css_class="mx-1 author-form",
            )
        )
AuthorFormset = forms.formset_factory(AuthorForm, extra=1)


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Div(Field('icon', css_class='form-control-sm'), css_class="col-12"),
                Div(Field('category', css_class='form-control-sm'), css_class="col-12"),
            )
        )

    class Meta:
        model = Category
        fields = ['icon', 'category']


class PostForm(forms.ModelForm):
    title = forms.CharField(label="Judul Karya atau Post", help_text="Tuliskan judul yang mudah diingat dan semenarik mungkin.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                # list of fields
                'title', 'image', 'video', 'document',
                Field('category', css_class='form-control form-control-sm'),
                'content',

                Div(
                    HTML('<div class="g-recaptcha" data-sitekey="6LegB3kcAAAAAC8G65G-cTAjArgI7xTJgL_OpNNH"></div>'),
                    HTML('<button type="submit" class="btn my-button align-self-center ms-4 mt-4">Unggah Karya!</button>'),
                    css_class='mt-4 d-flex flex-column flex-md-row align-items-center '
                ),
                # CSS Class for the row
                css_class='mx-1',
            ),
        )

    class Meta:
        model = Post
        exclude = ['verified', 'author', 'slug', 'v_yt_id', 'updated_at']

