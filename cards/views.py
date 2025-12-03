# cards/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from datetime import date

from .models import Card
from .forms import CardForm

@login_required
def cards_list(request):
    cards_qs = Card.objects.filter(user=request.user, activa=True)

    # Ordenar por próxima fecha límite real (urgencia)
    cards = sorted(cards_qs, key=lambda c: c.proxima_fecha_limite_real())

    next_to_pay = cards[0] if cards else None

    # Tarjeta recomendada (corte más lejano)
    recommended_card = None
    if cards_qs:
        recommended_card = sorted(
            cards_qs,
            key=lambda c: c.proxima_fecha_corte_real(),
            reverse=True
        )[0]

    # Fecha de hoy para cálculos
    hoy = date.today()

    # Calendario: solo eventos futuros o de hoy (los pagos pasados "desaparecen")
    eventos = []
    for card in cards_qs:
        fecha_corte = card.proxima_fecha_corte_real()
        fecha_pago = card.proxima_fecha_limite_real()

        if fecha_corte >= hoy:
            eventos.append({
                'fecha': fecha_corte,
                'tipo': 'Corte',
                'card': card,
            })
        if fecha_pago >= hoy:
            eventos.append({
                'fecha': fecha_pago,
                'tipo': 'Pago',
                'card': card,
            })

    eventos = sorted(eventos, key=lambda e: e['fecha'])

    # Notificaciones mensuales para recordar captura de pagos
    notificaciones = []
    for card in cards_qs:
        fecha_corte = card.proxima_fecha_corte_real()
        fecha_pago = card.proxima_fecha_limite_real()

        # Notificación especial el día de corte
        if fecha_corte == hoy:
            notificaciones.append({
                'tipo': 'corte',
                'card': card,
                'mensaje': (
                    f"Hoy es tu fecha de corte de la tarjeta {card.banco} – {card.nombre}. "
                    "Registra tu pago para evitar intereses."
                ),
            })
        # Durante el periodo entre corte y pago, recordatorio suave
        elif fecha_corte < hoy <= fecha_pago:
            notificaciones.append({
                'tipo': 'pago',
                'card': card,
                'mensaje': (
                    f"Estás en el periodo de pago de la tarjeta {card.banco} – {card.nombre}. "
                    "Asegúrate de registrar el monto que vas a pagar este mes."
                ),
            })

    context = {
        'cards': cards,
        'next_to_pay': next_to_pay,
        'recommended_card': recommended_card,
        'eventos': eventos,
        'notificaciones': notificaciones,
    }
    return render(request, 'cards/cards_list.html', context)

class InformacionTDCView(ListView):
    model = Card
    template_name = "cards/informacion_tdc.html"
    context_object_name = "tarjetas"

    def get_queryset(self):
        return Card.objects.filter(
            user=self.request.user,
            activa=True
        ).order_by("banco", "nombre")

@login_required
def card_create(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('cards_list')
    else:
        form = CardForm()

    return render(request, 'cards/card_form.html', {
        'form': form,
        'title': 'Agregar tarjeta'
    })


@login_required
def card_update(request, pk):
    card = get_object_or_404(Card, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect('cards_list')
    else:
        form = CardForm(instance=card)

    return render(request, 'cards/card_form.html', {
        'form': form,
        'title': 'Editar tarjeta'
    })


@login_required
def card_delete(request, pk):
    card = get_object_or_404(Card, pk=pk, user=request.user)
    if request.method == 'POST':
        card.activa = False   # en vez de borrarla
        card.save()
        return redirect('cards_list')

    return render(request, 'cards/card_confirm_delete.html', {'card': card})
