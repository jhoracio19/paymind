# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_remove_card_fecha_corte_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateField(help_text='Fecha límite de pago del periodo')),
                ('saldo_pagado', models.DecimalField(decimal_places=2, help_text='Saldo que tenía la tarjeta en ese periodo', max_digits=10)),
                ('monto_pagado', models.DecimalField(decimal_places=2, default=0, help_text='Monto que se pagó', max_digits=10)),
                ('pagado', models.BooleanField(default=False, help_text='Indica si el pago fue completado')),
                ('fecha_pagado', models.DateTimeField(blank=True, help_text='Fecha y hora en que se marcó como pagado', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_history', to='cards.card')),
            ],
            options={
                'verbose_name': 'Historial de pago',
                'verbose_name_plural': 'Historial de pagos',
                'ordering': ['-fecha_pago', '-created_at'],
            },
        ),
    ]

