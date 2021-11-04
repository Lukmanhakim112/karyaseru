from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Submit, Layout, Row,  
    Div, Field, HTML, Fieldset
)

from .models import Post, Category


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
            Row(
                Fieldset("Siapa yang Punya Karya?",
                    Row(
                        Div(Field('author', css_class='form-control-sm'), css_class="col-6"),
                        Div(Field('ig_account', css_class='form-control-sm'), css_class="col-6"),
                    ),
                    # Field('category', css_class='form-control form-control-sm'),
                    css_class='col-12 border-danger m-2 border rounded p-3'
                ),
                Fieldset( "Tuliskan Inspirasi Kamu!", # legend
                    # list of fields
                    'title', 'image', 'video', 'document',
                    Field('category', css_class='form-control form-control-sm'),
                    'content',

                    Div(
                        HTML('<div class="g-recaptcha" data-sitekey="6LegB3kcAAAAAC8G65G-cTAjArgI7xTJgL_OpNNH"></div>'),
                        HTML('<button type="submit" class="btn my-button align-self-center ms-4 mt-4">Unggah Karya!</button>'),
                        css_class='mt-4 d-flex flex-column flex-md-row align-items-center '
                    ),
                    css_class='col-12 border-danger m-2 p-3 border rounded'
                ),
                # CSS Class for the row
                css_class='',
            ),
        )

    class Meta:
        model = Post
        exclude = ['verified', 'slug', 'updated_at']
