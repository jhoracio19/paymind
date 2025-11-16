# PayMind

PayMind es una aplicación web sencilla para ayudar a usuarios con tarjetas de crédito a tomar mejores decisiones de pago y uso, sin depender de la app del banco.

## 🧱 Stack

- Python 3.x
- Django
- Django Templates
- Tailwind CSS (CDN)
- SQLite (desarrollo) – pensado para migrar a Postgres en producción

## 🎯 Objetivo del MVP v0.1

Versión mínima funcional que permita:

- Registrar tarjetas de crédito con datos básicos.
- Ver un **dashboard** con:
  - Próxima tarjeta a pagar.
  - Tarjeta recomendada para usar hoy (según próxima fecha de corte).
  - Calendario simple de cortes y pagos.
- CRUD completo de tarjetas por usuario autenticado.

## ⚙️ Setup del proyecto

### 1. Clonar repositorio

```bash
git clone <URL_DEL_REPO>
cd PayMind
