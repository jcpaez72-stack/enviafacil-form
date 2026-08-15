# 🛡️ MANIFIESTO DE FORMULARIOS EnvíaFácil 2.0 — FUENTE DE VERDAD

> **LEER ESTO ANTES DE TOCAR CUALQUIER FORMULARIO.** Cada feature listado abajo YA ESTÁ vivo en el archivo.
> Al hacer una actualización: **editar el archivo actual** (nunca regenerar desde cero) y **verificar que ninguno de estos ✅ se cayó** después del cambio.
> Cada feature tiene un *marcador* grepeable para verificar de un vistazo que sigue presente.
>
> Última actualización: 2026-07-22 (inventario derivado de los archivos reales, no de memoria).
>
> **Orden de update completo (obligatorio):** `laar-sandbox-cotizador/EF2-UPDATE-RUNBOOK.md`. Para workflows: `laar-sandbox-cotizador/WORKFLOWS-MANIFEST.md`.

## Cómo verificar que no hubo regresión
```bash
cd enviafacil-form-web
# corre esto después de CADA cambio; compara contra la tabla de abajo
for f in index.html datos-envio.html mapa.html oficina-retiro.html cotizador.html multienvio.html; do
  echo "── $f ──"
  grep -qi "EF_LOCK"        "$f" && echo "  ✅ candado"
  grep -qi "EF_EDIT"        "$f" && echo "  ✅ editable(nonce)"
  grep -qi "checkCiudad"    "$f" && echo "  ✅ control-ciudad"
  grep -qi "_rucOk"         "$f" && echo "  ✅ RUC/cedula"
  grep -qi "10,15"          "$f" && echo "  ✅ celular-intl"
  grep -qi "esDestino"      "$f" && echo "  ✅ destino-opcional"
  grep -qi "efBtnMapa"      "$f" && echo "  ✅ joya-mapa"
  grep -qi "sinJoya"        "$f" && echo "  ✅ ocultar-joya"
  grep -qi "ef_lat"         "$f" && echo "  ✅ lat/lon"
  grep -qi "flex-end"       "$f" && echo "  ✅ align-valor"
  grep -qi "calle_secundaria" "$f" && echo "  ✅ calle-sec"
  grep -qi "__EF_API_KEY__\|X-EF-Key" "$f" && echo "  ✅ seguridad-key"
done
```

## Estado actual por formulario (lo que DEBE seguir presente)

| Feature (marcador) | index | datos-envio | mapa | oficina-retiro | cotizador | multienvío |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Candado seguridad (`EF_LOCK`) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Editable con nonce (`EF_EDIT`/`EF_EDITLOCK`) | ✅ | ✅ | ✅ | ✅ | — *(JC: se pone cuando se use)* | ✅ |
| Control ciudad↔ubicación (`checkCiudad`/`efNorm`) | ✅ | — | ✅ | — | — | 🔴 |
| Validación cédula/RUC (`_rucOk`/`_mod11`/`_ced10`) | ✅ | — | — | — *(no captura id)* | — | ✅ |
| Celular internacional 10-15 díg (`/^\d{10,15}$/`) | ✅ | — | — | ✅ | — | ✅ |
| Destinatario correo/celular OPCIONAL (`esDestino`) | ✅ | — | — | — | — | 🔴 |
| Joya = mapa Leaflet in-form (`efBtnMapa`/`efMapaTop`) | ✅ | — | ✅ | — | — | ⚠️ |
| Ocultar joya si ya dio ubicación (`sinJoya`) | ✅ | — | — | — | — | 🔴 |
| Captura lat/lon (hidden `ef_lat`/`ef_lon` + prefill) | ✅ | — | ✅ | — | — | ✅ |
| Buscador Google Places / geocode | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Alineación Valor↔Peso (`align-items:flex-end`) | — | ✅ | — | — | — | — |
| Calle secundaria = campo propio (`calle_secundaria`) | ✅ | — | ✅ | — | — | ✅ |
| Seguridad API key (`__EF_API_KEY__` / `X-EF-Key`) | ✅ | ✅ | — | ✅ | ✅ | ✅ |

## Reglas que NUNCA deben regresar (con el *por qué*)

- **`calle_secundaria` se autocompleta SIEMPRE que el geocodificador devuelva sector** (`if(_cs)setV('calle_secundaria',_cs);`).
  **NUNCA** condicionarla al contenido de **otro** campo. *Por qué:* hasta el 22-jul-2026 dependía de que
  `referencia_recoleccion` estuviera vacío — un cruce entre campos distintos. Efecto: si el cliente ya tenía
  referencia (p. ej. precargada desde Datum), la calle secundaria **no se llenaba nunca**, y parecía un
  comportamiento aleatorio. Debe comportarse igual que `mapa.html`, que la manda sin condición.
- **Las coordenadas se guardan SIEMPRE**, incluso si el geocodificador falla
  (`setV('ef_lat',...)` va fuera del `if(d&&d.ok)`). El texto de la dirección puede quedar vacío; las
  coordenadas no. *Por qué:* es lo que viaja a LAAR y no puede perderse por un fallo de red.
1. **RUC de sociedades (3er díg 6/9): NO exigir mód 11 estricto.** El SRI emite RUC reales que no cumplen el checksum → mód11 estricto los rechaza. Usar salvaguarda por estructura (`_mod11(...)===dv || (+establecimiento)>0`). Probado con `0993384491001` y `0993378756001`. Ver [[laar-validacion-ruc-modulo10]].
2. **Celular: aceptar internacional (10-15 díg), no solo 10.** Un número USA de 11 díg atascaba el form. Prefill normaliza `593…`→`0…`. Ver [[laar-ef2-remitente-doble-tap-fix]].
3. **🔴 CORREGIDO 4-ago-2026 — el CELULAR del destinatario es OBLIGATORIO, 10 dígitos exactos.**
   Antes era opcional; el API `POST /api/Guias/v1/guias/contado` **rechaza con 400** sin
   `destino.celular` (*«Ingrese una número de celular»*), y la guía se genera **después de cobrar**:
   dos clientes pagaron y no recibieron nada (Patricia Montero $6,38 · Raúl Toapanta $6,74).
   **Doble barrera:** (a) el form lo exige; (b) el bot lo pide por chat si falta; (c) `&v=AAAAMMDD`
   en la URL o los teléfonos con el form en caché siguen mandándolo vacío.
   El **correo** del destinatario **sí sigue siendo opcional**. Ver [[laar-api-guia-exige-celular-destinatario]].
4. **Blindaje: si un dato viene inválido, el form NO debe atascar** — dejar vacío/pedir de nuevo, nunca quedar muerto ni desviar en silencio. Ver [[laar-ef2-degradacion-silenciosa]].
5. **Callback: URL absoluta a la función, SIN `X-EF-Key`** en el fetch del puente (rompía CORS de fenix). Ver [[laar-ef2-webview-callback-causa-raiz]].
6. **Candado + editable + re-candado:** al editar se abre solo lo editado; al cerrar se vuelve a poner candado. No dejar abierto.
7. **WebView WhatsApp: sin `confirm()`/`alert()`** (bloqueados); resolver por código. Ver [[referencia-webview-whatsapp-limites]].

## 📦 multienvio.html — agregado al manifiesto el 15-ago-2026
Se creó después de este documento y **nunca estuvo aquí**: por eso nadie corrió la verificación sobre él.
- **Canónico:** `multienvio.html` (no tiene gemelo `-fenix`; se entrega con el mismo nombre).
- **Publicado por LAAR como** `multienvio-prueba.html`; `multienvio.html` da 404 (aún no definitivo).
- **Propio de este form (no está en los otros):** dos pasos en un archivo (`?paso=remitente` /
  `?paso=destinos`), **la ciudad se elige DENTRO** (por eso `checkCiudad` hay que adaptarlo, no copiarlo),
  bandera **`uno=1`** = confirma UN destino y cierra (el chat pregunta si va otro).
- 🔴 **Deudas abiertas al 15-ago:** celular del destinatario obligatorio · `&v=` en sus URLs ·
  `checkCiudad` · `sinJoya`.

## ⚠️ Riesgo de regresión detectado — ARCHIVOS DUPLICADOS
En la carpeta hay variantes que pueden confundir cuál es el "bueno":
- **CANÓNICOS (editar estos):** `index.html`, `datos-envio.html`, `mapa.html`, `oficina-retiro.html`, `cotizador.html`.
- **`*-fenix.html`** (index-fenix, datos-envio-fenix, cotizador-fenix, oficina-retiro-fenix): copias para el server de LAAR. **Al actualizar un canónico, regenerar su -fenix** o quedan desincronizados.
- **Sueltos/viejos** (`envio.html`, `remitente.html`, `oficinas.html`, `test.html`): verificar si son legado antes de reusarlos. **NO partir de estos.**

## Flujo Jelou asociado (dónde se cablean las URLs de estos forms)
- `ef2-recoleccion-de-datos` (wf **57956** / skill **41636**): remitente + destinatario. Fix doble-tap remitente aplicado 22-jul (ver [[laar-ef2-remitente-doble-tap-fix]]).
- `ef2-info-tipo-paquete` (wf **57955** / skill **41635**): datos-envío + cotización (impresionGuias boolean).
- URLs webview pasan `&ciudadEsp=…&provEsp=…&sinJoya=…&edit=…&v=…` (cache-bust).


## ✅ -fenix SINCRONIZADOS (2026-07-21)
Regenerados los 5 -fenix desde canónico (todos fenix-ready, 0 github). Creado mapa-fenix (no existía). Paquete de entrega a LAAR: `entrega-fenix-forms-20260721/` (nombres base + LEEME con changelog y nota CSP: permitir unpkg.com + tile.openstreetmap.org + enviafacil-geocode/callback .fn.jelou.ai).
