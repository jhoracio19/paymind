from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    banco = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

    limite_credito = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_actual = models.DecimalField(max_digits=10, decimal_places=2)

    # Día del mes (1-31)
    fecha_corte = models.PositiveSmallIntegerField()
    fecha_limite_pago = models.PositiveSmallIntegerField()

    anualidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Ej: #FFD700
    color = models.CharField(max_length=7, help_text="Color HEX, ej: #FFD700")

    created_at = models.DateTimeField(auto_now_add=True)
    
    def proxima_fecha_limite_real(self):
        hoy = date.today()

        # Fecha del mes actual con el día de la tarjeta
        fecha = date(hoy.year, hoy.month, self.fecha_limite_pago)

        # Si ya pasó, mover al siguiente mes
        if fecha < hoy:
            # Si estás en diciembre, pasa al siguiente año
            if hoy.month == 12:
                fecha = date(hoy.year + 1, 1, self.fecha_limite_pago)
            else:
                fecha = date(hoy.year, hoy.month + 1, self.fecha_limite_pago)

        return fecha
    
    def proxima_fecha_corte_real(self):
        hoy = date.today()
        fecha = date(hoy.year, hoy.month, self.fecha_corte)
        if fecha < hoy:
            if hoy.month == 12:
                fecha = date(hoy.year + 1, 1, self.fecha_corte)
            else:
                fecha = date(hoy.year, hoy.month + 1, self.fecha_corte)
        return fecha


    def __str__(self):
        return f"{self.banco} - {self.nombre}"
