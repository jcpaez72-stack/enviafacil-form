# EnvíaFácil — Actualización de formularios (30-jul-2026)

Reemplazar los 5 archivos en `fenix.laarcourier.com/EnvioFacil/` (mismos nombres).
**Recomendado:** respaldar los actuales antes de sobrescribir.

---

## Qué se corrige

### 1. Candado de formularios: ahora funciona en cualquier dispositivo 🔴 (principal)

**Problema detectado:** el candado que impide volver a llenar un formulario ya enviado
se guardaba **solo en el navegador donde se llenó**. Si el cliente completaba el
formulario en la computadora y luego lo reabría desde el celular (o al revés), el
candado no aparecía y **podía volver a llenarlo y reenviarlo**, incluso sobre un envío
ya procesado.

**Solución:** el registro de "ya enviado" pasa a un servicio central. El formulario
consulta al abrirse y bloquea en **cualquier** teléfono, computadora o navegador.

- Al enviar correctamente → se registra la conversación + formulario.
- Al abrir → se consulta; si ya fue enviado, muestra *"Datos ya enviados"*.
- **Si el servicio no responde**, el formulario **NO se bloquea** (se usa el candado
  local como antes): nunca se traba a un cliente por un problema de red.
  Se muestra un "Verificando…" de máximo 4 segundos.
- El botón **"Editar datos"** del chat sigue funcionando igual (la edición autorizada
  por el bot no se bloquea).

### 2. Número de WhatsApp por defecto → producción

El botón *"Volver a WhatsApp"* tenía como valor por defecto el número de **pruebas**
(`593999842656`). Hoy no afectaba porque el bot siempre envía el número en el enlace,
pero si ese dato faltara, el cliente escribiría a un número sin atención.
Corregido a **`593991344747`** en los 5 archivos.

---

## Requisito técnico (importante)

Los formularios consultan este servicio:

```
https://enviafacil-formlock.fn.jelou.ai
```

Si el servidor aplica una política de contenido (CSP) o un firewall de salida,
**debe permitirse ese dominio** (`*.fn.jelou.ai`), igual que ya se permite
`enviafacil-callback.fn.jelou.ai` y `enviafacil-geocode.fn.jelou.ai`.
Sin ese permiso el candado nuevo no bloqueará (el formulario seguirá funcionando
normal, con el candado local de siempre).

---

## Qué NO cambió

- Ninguna validación de campos (cédula/RUC, celular, ciudad, obligatorios).
- El diseño y el flujo de los formularios.
- La conexión con el bot (el envío de datos sigue igual).
- Las claves y credenciales: los archivos traen los marcadores `__EF_API_KEY__` y
  `__AI_CONNECTION_STRING__`, que deben reemplazarse como en despliegues anteriores.

---

## Cómo probar (5 minutos)

1. Iniciar un envío desde WhatsApp y completar el formulario del **destinatario**
   **desde una computadora**.
2. Volver al chat y tocar **el mismo botón del formulario desde un celular**.
   → Debe mostrar **"Datos ya enviados. Esta información ya fue registrada"**.
   *(Antes de este cambio, se abría vacío y permitía llenarlo de nuevo.)*
3. Iniciar un envío nuevo con otro cliente → el formulario debe abrirse normal.
4. Usar **"Editar datos"** desde el chat → debe permitir editar.

---

## Archivos

| Archivo | Cambios |
|---|---|
| `index.html` | candado central + número de producción |
| `datos-envio.html` | candado central + número de producción |
| `cotizador.html` | candado central + número de producción |
| `oficina-retiro.html` | candado central + número de producción |
| `mapa.html` | candado central + número de producción |

Contacto: Juan Carlos Páez.
