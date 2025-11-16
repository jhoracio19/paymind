from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('banco', 'nombre', 'user', 'limite_credito', 'saldo_actual')
    list_filter = ('banco', 'user')
