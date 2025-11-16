from django.db import models
from django.contrib.auth.models import User


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

    def __str__(self):
        return f"{self.banco} - {self.nombre}"
