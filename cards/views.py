# cards/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Card
from .forms import CardForm


@login_required
def cards_list(request):
    cards = Card.objects.filter(user=request.user)
    cards = sorted(cards, key=lambda c: c.proxima_fecha_limite_real())
    return render(request, 'cards/cards_list.html', {'cards': cards})


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
