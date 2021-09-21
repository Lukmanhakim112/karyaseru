from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Submit, Layout, Fieldset,
    Row, Div, Field, HTML
)

from .models import Post, Category


class PostForm(forms.ModelForm):
    title = forms.CharField(label="Judul Karya atau Post", help_text="Tuliskan judul yang mudah diingat dan semenarik mungkin.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '', # The first argument is a legend
                Row(
                    Div(
                        Field('author', css_class='form-control-sm'),
                        Field('ig_account', css_class='form-control-sm'),
                        Field('category', css_class='form-control form-control-sm'),
                        css_class='col m-2 border rounded p-3'
                    ),
                    Div(
                        'title', 'image', 'content',
                        Div(
                            HTML('<div class="g-recaptcha" data-sitekey="6LegB3kcAAAAAC8G65G-cTAjArgI7xTJgL_OpNNH"></div>'),
                            HTML('<button type="submit" class="btn my-button m-1 mt-4">Unggah Karya!</button>'),
                            css_class='mt-4'
                        ),
                        css_class='col-9 m-2 p-3 border rounded'
                    ),
                    # CSS Class for the row
                    css_class='',
                ),
            )
        )

    class Meta:
        model = Post
        exclude = ['slug', 'updated_at']
