from django.urls import path
from .views import cards_list, card_create, card_update, card_delete

urlpatterns = [
    path('', cards_list, name='cards_list'),
    path('cards/nueva/', card_create, name='card_create'),
    path('cards/<int:pk>/editar/', card_update, name='card_update'),
    path('cards/<int:pk>/eliminar/', card_delete, name='card_delete'),
]