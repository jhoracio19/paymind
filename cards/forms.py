from django import forms
from .models import Card


BASE_INPUT_CLASSES = (
    "w-full px-3 py-2 rounded-lg border border-slate-300 text-sm "
    "focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
)


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ['user', 'created_at']

        widgets = {
            'banco': forms.TextInput(attrs={'class': BASE_INPUT_CLASSES}),
            'nombre': forms.TextInput(attrs={'class': BASE_INPUT_CLASSES}),
            'limite_credito': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'step': '0.01',
            }),
            'saldo_actual': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'step': '0.01',
            }),
            'fecha_corte': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'min': 1,
                'max': 31,
            }),
            'fecha_limite_pago': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'min': 1,
                'max': 31,
            }),
            'anualidad': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'step': '0.01',
            }),
            'color': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'placeholder': '#FFD700',
            }),
        }
