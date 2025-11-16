from django import forms
from .models import Card


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ['user', 'created_at']
