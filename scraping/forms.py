from django import forms
from .models import *


class FindForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label='Город не выбран',
        to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Город'
    )

    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        empty_label='Специальность не выбрана',
        to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Специальность'
    )
