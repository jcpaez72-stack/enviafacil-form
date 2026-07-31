# EnvíaFácil — Actualización de formularios

Reemplazar los 5 archivos en `fenix.laarcourier.com/EnvioFacil/` (mismos nombres).
**Recomendado:** respaldar los actuales antes de sobrescribir.

> **Base:** estos archivos se construyeron **sobre los que ustedes tienen hoy en producción**
> (descargados de fenix), así que **conservan íntegro su monitoreo de Application Insights** y todos
> sus ajustes previos. Los marcadores `__EF_API_KEY__` y `__AI_CONNECTION_STRING__` se reemplazan
> como en despliegues anteriores.

---

## 1. Candado de formularios en cualquier dispositivo 🔴 (lo principal)

**Problema:** el candado que impide volver a llenar un formulario ya enviado se guardaba **solo en el
navegador donde se completó**. Si el cliente llenaba en la computadora y luego reabría desde el celular
(o al revés), el formulario **se abría vacío y podía reenviarse**, incluso sobre un envío ya procesado.

**Solución:** el registro de "ya enviado" pasa a un servicio central; el formulario consulta al abrirse
y bloquea en **cualquier** teléfono, computadora o navegador.

- **Si el servicio no responde, el formulario NO se bloquea** (usa el candado local de antes): nunca se
  traba a un cliente por un problema de red.
- El botón **"Editar datos"** del chat sigue funcionando igual.

### ⚙️ Requisito de su lado
Los formularios consultan `https://enviafacil-formlock.fn.jelou.ai`.
Si aplican política de contenido (CSP) o firewall de salida, **debe permitirse ese dominio**
(`*.fn.jelou.ai`), igual que ya permiten `enviafacil-callback` y `enviafacil-geocode`.
Sin ese permiso el formulario funciona normal, pero el candado nuevo no bloqueará.

---

## 2. Cotizador: tres reglas que estaban solo en "Datos del envío"

Al comparar ambos formularios encontramos que **tres validaciones se habían aplicado solo a
*Datos del envío*** y al **Cotizador** se le habían quedado. Ahora los dos aplican lo mismo:

| Regla | Antes en el Cotizador | Ahora |
|---|---|---|
| **Peso máximo** | 50 kg **por envío** | **50 kg por pieza** ✅ |
| **Valor declarado** | no se pedía | **obligatorio (> 0)** en Paquete ✅ |
| **Tipo de contenido** | no existía | **obligatorio** en Paquete ✅ |

**Impacto real del tope de peso:** una carga de 3 bultos de 40 kg (120 kg) **no se podía cotizar**,
pero sí se podía completar el envío. Ahora es coherente.

**Por qué agregamos "Tipo de contenido":** si el cliente cotiza y luego decide enviar, ya no habrá que
volver a pedirle esa información.

> 📄 **La regla de Documento no cambió:** sigue pidiendo solo origen y destino. El peso (2 kg), el valor (0),
> el contenido y la pieza (1) se envían automáticamente, y esos campos permanecen ocultos.

---

## 3. Botón "Editar" en la pantalla de confirmación

En el formulario de remitente/destinatario, la pantalla de revisión solo tenía **Confirmar**: si el
cliente se equivocaba (p. ej. en la cédula), **no tenía cómo corregir**. Ahora aparece **"✏️ Editar"**
junto a Confirmar, que devuelve al formulario **conservando todo lo escrito**.

---

## 4. Mejoras menores

- **Asterisco de obligatorio** en las etiquetas de ciudades, piezas, peso, valor y contenido (antes el
  cliente lo descubría al intentar continuar). *Solo la etiqueta; las validaciones no cambiaron.*
- **Aviso de espera:** si el envío tarda más de 5 segundos, el botón muestra *"Enviando… no cierres esta
  ventana"*, para que el cliente no cierre creyendo que se colgó. **No se corta ni se reintenta el envío**
  (para evitar cualquier riesgo de duplicado).
- **Número de WhatsApp por defecto:** corregido al de producción (**099 134 4747**). Antes tenía el de
  pruebas; no afectaba porque el bot siempre envía el número, pero si faltara, el cliente escribiría a un
  número sin atención.
- **Menos preguntas repetidas:** si el cliente ya indicó qué contiene su paquete al cotizar, *Datos del envío*
  ahora puede recibirlo precargado (parámetro `preContenido`, igual que el peso y las piezas). Si no llega,
  el campo queda vacío como hasta hoy.
- **Registro de diagnóstico:** si el cotizador se abre **sin el tipo de envío** (señal de que algo falló
  antes), queda registrado en su Application Insights como `EF_cotizador_sin_tipo`. El cliente no ve nada.

---

## Qué NO cambió

- Ninguna validación existente (cédula/RUC, celular, ciudades, obligatorios).
- El diseño ni el flujo de los formularios.
- La conexión con el bot (el envío de datos sigue igual).
- Su monitoreo de Application Insights.

---

## Cómo probar (10 minutos)

1. **Candado entre dispositivos:** completar el formulario del **destinatario desde una computadora**;
   luego, en el chat, tocar **ese mismo botón desde un celular** → debe mostrar *"Datos ya enviados"*.
   *(Antes se abría vacío.)*
2. **Cliente nuevo:** iniciar un envío distinto → el formulario debe abrirse normal.
3. **Editar:** llenar el formulario, tocar **Continuar** y luego **✏️ Editar** → debe volver con los datos
   y permitir corregir.
4. **Cotizador (Paquete):** debe aparecer *Tipo de contenido* (obligatorio) y pedir valor declarado.
   Probar **3 piezas de 40 kg** → debe **cotizar** (antes lo rechazaba). Probar **1 pieza de 60 kg** →
   debe avisar *"máximo 50 kg por pieza"*.
5. **Cotizador (Documento):** no debe pedir peso, valor ni contenido.

Contacto: Juan Carlos Páez.
