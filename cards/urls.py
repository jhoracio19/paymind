from django.urls import path
from .views import cards_list, card_create, card_update, card_delete, InformacionTDCView, mark_payment_paid, payment_history, mark_card_payment_paid

urlpatterns = [
    path('', cards_list, name='cards_list'),
    path('cards/nueva/', card_create, name='card_create'),
    path('cards/<int:pk>/editar/', card_update, name='card_update'),
    path('cards/<int:pk>/eliminar/', card_delete, name='card_delete'),
    path("info-tdc/", InformacionTDCView.as_view(), name="info_tdc"),
    path('cards/pagos/<int:historial_id>/marcar-pagado/', mark_payment_paid, name='mark_payment_paid'),
    path('cards/<int:card_id>/marcar-pago/', mark_card_payment_paid, name='mark_card_payment_paid'),
    path('historial/', payment_history, name='payment_history'),
]