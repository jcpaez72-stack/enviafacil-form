# Pago en la web — lo que ya está habilitado (extraído de los correos de Nuvei y De Una)

⛔ **Ninguna credencial se copia en este archivo.** Van como secretos. Aquí solo el mapa técnico.

---

## Opción 1 — Nuvei **Link to Pay** ⭐ recomendada para tarjeta

Es una **página de pago alojada por Nuvei**: nuestro servidor crea la orden, Nuvei devuelve un
`payment_url`, el cliente paga allá y vuelve. **La tarjeta nunca toca nuestra página ni nuestro servidor.**

| | |
|---|---|
| Doc | `https://developers.paymentez.com/api/#payment-methods-linktopay` |
| Crear orden | `POST https://noccapi-stg.paymentez.com/linktopay/init_order/` *(stg = pruebas)* |
| Respuesta | `data.payment.payment_url` → ahí se manda al cliente |
| Estado del pago | **webhook** (`#webhook`) → **hay que darles una URL nuestra para las notificaciones** |
| 3DS | ✅ soportado |
| Credenciales PRODUCCIÓN | `LAARCOURIERLTP-EC-CLIENT` / `LAARCOURIERLTP-EC-SERVER` (appkeys en Excel cifrado) |
| Credenciales DEV | en el correo de Nuvei del 16-jul → **se puede desarrollar YA** |
| Tarjetas de prueba | `4111111111111111` aprueba · `4242424242424242` rechaza · exp 11/27 · CVV 634 |

Cuerpo de la orden: `user{id,email,name,last_name}` · `order{dev_reference,description,amount,vat,
tax_percentage,taxable_amount,installments_type,currency}` · `configuration{expiration_time,
allowed_payment_methods,success_url,failure_url,pending_url,review_url}`.

## Opción 2 — Nuvei **Checkout** (sitio web)
Credencial creada el 19-jul: **`LAARCOURIEREXPRESS-JELOU-EC`** · 3DS 2.0 ✅ · OTP ✅ ·
red principal **Medianet**, secundaria **Datafast**. Nuvei lo describe como *"método recomendado para pagos
únicos"*. Alternativa a Link to Pay; también es página alojada.

## Opción 3 — **De Una** (pago desde la app del banco) ⭐ la más simple
Sin tarjetas de por medio → **cero riesgo de datos de tarjeta**.

| | |
|---|---|
| Crear cobro | `POST https://apis-merchant.pdn.deunalab.com/merchant/v1/payment/request` |
| Consultar | `/payment/info` · anular `/payment/cancel` · reversar `/payment/void` · devolver `/payment/refund` |
| Auth | `x-api-key` / `x-api-secret` (producción, entregadas 1-may) |
| POS | RUC 1791705726001 · LAARCOURIER · sucursal **ENVIA FACIL** 225354 · caja 225355 |
| Ambiente de pruebas | ❓ **no consta** — pedirlo a Pichincha (las URLs `pdn` son PRODUCCIÓN) |

---

## 🔴 Restricciones del negocio que afectan al diseño

1. **Límite máximo de compra: $300** (ambas credenciales Nuvei).
   ⚠️ **Un multidestino con varios destinos puede superarlo.** Hay que decidir: ¿se pide ampliación a Nuvei,
   se parte el cobro, o se limita el número de destinos por pedido?
2. **Límite quincenal de ~10 transacciones por usuario** (mencionado por Nuvei en mayo; confirmar si sigue).
3. ⚠️ **«Cualquier transacción de prueba que no sea reversada será facturada al comercio»** → **desarrollar
   contra `stg`**, nunca contra producción.
4. Solo se procesan **transacciones autenticadas** (3DS obligatorio).

## Lo que hay que pedir
- **URL de webhook**: se la debemos dar a Nuvei (la hospedamos nosotros en una función).
- **Contraseña del Excel cifrado** con los appkeys de producción → **no por chat**, se cargan como secretos.
- **Ambiente de pruebas de De Una**, si existe.
- **Ampliación del límite de $300** si el multidestino lo requiere.

## Recomendación
**Arrancar con Link to Pay (tarjeta) + De Una (app)**, ambas como páginas alojadas por el proveedor.
Se puede **empezar a construir hoy** con las credenciales DEV de Link to Pay y las tarjetas de prueba,
sin depender de nadie.
