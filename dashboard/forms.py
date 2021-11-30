from django import forms


from blog.models import Post

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Div, Field
)



class PostFormDashboard(forms.ModelForm):
    title = forms.CharField(label="Judul Karya atau Post", help_text="Tuliskan judul yang mudah diingat dan semenarik mungkin.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                # list of fields
                'title',
                Field('author', css_class='form-control form-control-sm'),
                'image', 'video', 'document',
                Field('category', css_class='form-control form-control-sm'),
                'content',

                # CSS Class for the row
                css_class='mx-1',
            ),
        )

    class Meta:
        model = Post
        exclude = ['verified', 'slug', 'v_yt_id', 'updated_at']

