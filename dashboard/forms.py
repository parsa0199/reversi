from django import forms
from .models import SellControl


class SellControlForm(forms.ModelForm):
    class Meta:
        model = SellControl
        fields = ('is_open', )