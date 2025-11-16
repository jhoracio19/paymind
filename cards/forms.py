from django import forms
from .models import Card
import re


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
            'limite_credito': forms.NumberInput(attrs={'class': BASE_INPUT_CLASSES, 'step': '0.01'}),
            'saldo_actual': forms.NumberInput(attrs={'class': BASE_INPUT_CLASSES, 'step': '0.01'}),
            'fecha_corte': forms.NumberInput(attrs={'class': BASE_INPUT_CLASSES, 'min': 1, 'max': 31}),
            'fecha_limite_pago': forms.NumberInput(attrs={'class': BASE_INPUT_CLASSES, 'min': 1, 'max': 31}),
            'anualidad': forms.NumberInput(attrs={'class': BASE_INPUT_CLASSES, 'step': '0.01'}),
            'color': forms.TextInput(attrs={'class': BASE_INPUT_CLASSES, 'placeholder': '#FFD700'}),
        }

    def clean_fecha_corte(self):
        dia = self.cleaned_data['fecha_corte']
        if dia < 1 or dia > 31:
            raise forms.ValidationError("El día de corte debe estar entre 1 y 31.")
        return dia

    def clean_fecha_limite_pago(self):
        dia = self.cleaned_data['fecha_limite_pago']
        if dia < 1 or dia > 31:
            raise forms.ValidationError("El día de pago debe estar entre 1 y 31.")
        return dia

    def clean_limite_credito(self):
        limite = self.cleaned_data['limite_credito']
        if limite <= 0:
            raise forms.ValidationError("El límite de crédito debe ser mayor a 0.")
        return limite

    def clean_saldo_actual(self):
        saldo = self.cleaned_data['saldo_actual']
        if saldo < 0:
            raise forms.ValidationError("El saldo no puede ser negativo.")
        return saldo

    def clean_anualidad(self):
        anualidad = self.cleaned_data.get('anualidad')
        if anualidad is not None and anualidad < 0:
            raise forms.ValidationError("La anualidad no puede ser negativa.")
        return anualidad

    def clean_color(self):
        color = self.cleaned_data['color']
        if not re.match(r'^#[0-9A-Fa-f]{6}$', color):
            raise forms.ValidationError("Usa un color HEX válido, por ejemplo: #FFD700.")
        return color