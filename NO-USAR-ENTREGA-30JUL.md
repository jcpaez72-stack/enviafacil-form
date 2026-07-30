# ⛔ NO USAR — entrega del 30-jul-2026 (candado server-side)

Esta entrega **rompió el cotizador en producción** y fue revertida por LAAR.

**Bug:** el código del candado usa la variable `EF_EDIT`, que **`cotizador.html` NO define**
→ ReferenceError → muere el resto del script → el formulario no avanza.
Solo se manifiesta **con `executionId`** (como lo abre el bot).

**Además:**
- Los archivos partieron de este banco, que estaba **desincronizado con producción**: les
  faltaba el bloque de **monitoreo Azure** que LAAR ya tenía → la entrega se lo borraba.
- Se introdujo una **pantalla "Verificando…"** (elemento `efVerif`) visible al abrir,
  sin alertar ni aprobar. Solo estaba aprobado tocar seguridad.

**Antes de retomar:** leer `regla-no-entregar-sin-diff-contra-produccion` en la memoria.
Los `-fenix` de esta carpeta YA fueron sincronizados con lo que LAAR tiene vivo.
