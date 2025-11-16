# cards/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Card
from .forms import CardForm


@login_required
def cards_list(request):
    cards_qs = Card.objects.filter(user=request.user)

    # Lista ordenada por urgencia (fecha límite real más cercana)
    cards = sorted(cards_qs, key=lambda c: c.proxima_fecha_limite_real())

    # Próxima tarjeta a pagar
    next_to_pay = cards[0] if cards else None

    # Tarjeta recomendada para usar hoy (la que tiene el corte más lejano)
    recommended_card = None
    if cards_qs:
        recommended_card = sorted(
            cards_qs,
            key=lambda c: c.proxima_fecha_corte_real(),
            reverse=True
        )[0]

    # Calendario simple: lista de eventos (corte / pago)
    eventos = []
    for card in cards_qs:
        eventos.append({
            'fecha': card.proxima_fecha_corte_real(),
            'tipo': 'Corte',
            'card': card,
        })
        eventos.append({
            'fecha': card.proxima_fecha_limite_real(),
            'tipo': 'Pago',
            'card': card,
        })

    eventos = sorted(eventos, key=lambda e: e['fecha'])

    context = {
        'cards': cards,
        'next_to_pay': next_to_pay,
        'recommended_card': recommended_card,
        'eventos': eventos,
    }
    return render(request, 'cards/cards_list.html', context)


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
    return render(request, 'cards/card_form.html', {'form': form, 'title': 'Agregar tarjeta'})


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
    return render(request, 'cards/card_form.html', {'form': form, 'title': 'Editar tarjeta'})


@login_required
def card_delete(request, pk):
    card = get_object_or_404(Card, pk=pk, user=request.user)
    if request.method == 'POST':
        card.delete()
        return redirect('cards_list')
    return render(request, 'cards/card_confirm_delete.html', {'card': card})
