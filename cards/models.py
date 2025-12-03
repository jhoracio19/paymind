from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')

    banco = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

    limite_credito = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Día del mes (1–31)
    dia_corte = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(31)]
    )
    dia_limite_pago = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(31)]
    )

    anualidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    color = models.CharField(max_length=7, help_text="Color HEX, ej: #FFD700")

    activa = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # ==============================================================
    # Métodos: próxima fecha real (construida a partir del día)
    # ==============================================================

    def proxima_fecha_limite_real(self):
        hoy = date.today()
        dia = self.dia_limite_pago

        # Construye fecha tentativa
        fecha = date(hoy.year, hoy.month, dia)

        # Si ya pasó, mover al siguiente mes
        if fecha < hoy:
            if hoy.month == 12:
                fecha = date(hoy.year + 1, 1, dia)
            else:
                fecha = date(hoy.year, hoy.month + 1, dia)

        return fecha

    def proxima_fecha_corte_real(self):
        hoy = date.today()
        dia = self.dia_corte

        fecha = date(hoy.year, hoy.month, dia)

        if fecha < hoy:
            if hoy.month == 12:
                fecha = date(hoy.year + 1, 1, dia)
            else:
                fecha = date(hoy.year, hoy.month + 1, dia)

        return fecha

    def __str__(self):
        return f"{self.banco} - {self.nombre}"
