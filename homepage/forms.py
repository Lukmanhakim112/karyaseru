from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Submit, Layout, Row,  
    Div, Field, HTML, Fieldset
)

from .models import Homepage



class HomepageForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Div(Field('slogan', css_class='form-control-sm'), css_class="col-12"),
                Div(Field('expl', css_class='form-control-sm'), css_class="col-12"),
            ),
        )

    class Meta:
        model = Homepage
        fields = '__all__'
