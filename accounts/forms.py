from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Clases para todos los inputs
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": (
                    "w-full px-3 py-2 rounded-lg border border-slate-300 "
                    "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                    "focus:border-indigo-500 transition text-sm"
                )
            })
