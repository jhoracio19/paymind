# cards/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import date, timedelta

from .models import Card, PaymentHistory
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
    pagos_pendientes = []
    
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
        
        # Verificar si hay pagos pendientes (fecha de pago ya pasó)
        # Si la fecha de pago es futura, calcular la del periodo anterior
        fecha_pago_anterior = fecha_pago
        if fecha_pago >= hoy:
            # Calcular la fecha de pago del mes anterior
            if fecha_pago.month == 1:
                fecha_pago_anterior = date(fecha_pago.year - 1, 12, min(card.dia_limite_pago, 28))
            else:
                # Asegurar que el día sea válido para el mes anterior
                mes_anterior = fecha_pago.month - 1
                dia_valido = min(card.dia_limite_pago, 28)  # Usar 28 para evitar problemas con meses de 30/31 días
                fecha_pago_anterior = date(fecha_pago.year, mes_anterior, dia_valido)
        
        # Si la fecha de pago anterior ya pasó y hay saldo, crear/verificar historial
        if fecha_pago_anterior < hoy and card.saldo_actual > 0:
            # Verificar si ya existe un registro de historial para este periodo
            historial_existente = PaymentHistory.objects.filter(
                card=card,
                fecha_pago=fecha_pago_anterior
            ).first()
            
            if not historial_existente:
                # Crear registro de historial si no existe
                historial_existente = PaymentHistory.objects.create(
                    card=card,
                    fecha_pago=fecha_pago_anterior,
                    saldo_pagado=card.saldo_actual,
                    pagado=False
                )
            
            if not historial_existente.pagado:
                pagos_pendientes.append({
                    'card': card,
                    'fecha_pago': fecha_pago_anterior,
                    'saldo': card.saldo_actual,
                    'historial_id': historial_existente.id,
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

    # Datos para el gráfico de dona (crédito total por tarjeta)
    chart_data = []
    total_credito = 0
    for card in cards_qs:
        limite = float(card.limite_credito)
        total_credito += limite
        chart_data.append({
            'label': f"{card.banco} - {card.nombre}",
            'value': limite,
            'color': card.color,
        })

    context = {
        'cards': cards,
        'next_to_pay': next_to_pay,
        'recommended_card': recommended_card,
        'eventos': eventos,
        'notificaciones': notificaciones,
        'chart_data': chart_data,
        'total_credito': total_credito,
        'pagos_pendientes': pagos_pendientes,
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


@login_required
@require_POST
def mark_payment_paid(request, historial_id):
    """Marca un pago como completado y resetea el saldo de la tarjeta"""
    historial = get_object_or_404(PaymentHistory, id=historial_id, card__user=request.user)
    
    if not historial.pagado:
        # Marcar como pagado
        historial.pagado = True
        historial.fecha_pagado = timezone.now()
        historial.monto_pagado = historial.saldo_pagado
        historial.save()
        
        # Resetear el saldo de la tarjeta
        card = historial.card
        card.saldo_actual = 0
        card.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Pago de {card.banco} - {card.nombre} marcado como completado.'
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Este pago ya fue marcado como completado.'
    }, status=400)


@login_required
@require_POST
def mark_card_payment_paid(request, card_id):
    """Marca el pago de una tarjeta como completado directamente desde la lista"""
    card = get_object_or_404(Card, pk=card_id, user=request.user, activa=True)
    
    if card.saldo_actual <= 0:
        return JsonResponse({
            'success': False,
            'message': 'Esta tarjeta no tiene saldo pendiente.'
        }, status=400)
    
    # Calcular la fecha de pago del periodo actual
    hoy = date.today()
    fecha_pago = card.proxima_fecha_limite_real()
    
    # Si la fecha de pago es futura, usar la del mes anterior
    if fecha_pago >= hoy:
        if fecha_pago.month == 1:
            fecha_pago_periodo = date(fecha_pago.year - 1, 12, min(card.dia_limite_pago, 28))
        else:
            mes_anterior = fecha_pago.month - 1
            dia_valido = min(card.dia_limite_pago, 28)
            fecha_pago_periodo = date(fecha_pago.year, mes_anterior, dia_valido)
    else:
        fecha_pago_periodo = fecha_pago
    
    # Buscar o crear el registro de historial
    historial, created = PaymentHistory.objects.get_or_create(
        card=card,
        fecha_pago=fecha_pago_periodo,
        defaults={
            'saldo_pagado': card.saldo_actual,
            'monto_pagado': card.saldo_actual,
            'pagado': True,
            'fecha_pagado': timezone.now(),
        }
    )
    
    if not created and not historial.pagado:
        # Si ya existía pero no estaba pagado, actualizarlo
        historial.pagado = True
        historial.fecha_pagado = timezone.now()
        historial.monto_pagado = card.saldo_actual
        historial.saldo_pagado = card.saldo_actual
        historial.save()
    
    # Resetear el saldo de la tarjeta
    card.saldo_actual = 0
    card.save()
    
    return JsonResponse({
        'success': True,
        'message': f'Pago de {card.banco} - {card.nombre} marcado como completado.',
        'redirect_url': '/historial/'
    })


@login_required
def payment_history(request):
    """Vista del historial de pagos"""
    cards_qs = Card.objects.filter(user=request.user, activa=True)
    historial = PaymentHistory.objects.filter(
        card__in=cards_qs
    ).select_related('card').order_by('-fecha_pago', '-created_at')
    
    # Agrupar por mes y año
    historial_por_mes = {}
    for pago in historial:
        mes_key = pago.fecha_pago.strftime('%Y-%m')
        if mes_key not in historial_por_mes:
            historial_por_mes[mes_key] = []
        historial_por_mes[mes_key].append(pago)
    
    # Calcular estadísticas
    total_registros = historial.count()
    pagos_completados = historial.filter(pagado=True).count()
    total_pagado = sum(float(p.monto_pagado) for p in historial if p.pagado)
    
    context = {
        'historial': historial,
        'historial_por_mes': historial_por_mes,
        'total_registros': total_registros,
        'pagos_completados': pagos_completados,
        'total_pagado': total_pagado,
    }
    return render(request, 'cards/payment_history.html', context)
