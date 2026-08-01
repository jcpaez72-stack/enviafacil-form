# EnvíaFácil Web — qué necesitamos de LAAR

**Modelo acordado (TICs, 1-ago):** nosotros desarrollamos **todo**; LAAR **publica los archivos en sus
servidores** y expone **una sola URL** que llaman desde un botón de su web.
**Alcance elegido por JC: el cliente PAGA EN LA WEB** (no solo arma el envío).

---

## 🔴 BLOQUEA EL DESARROLLO — sin esto no se puede avanzar

### 1. Cobro web
- ¿Con qué pasarela cobra LAAR **en su web**: **Nuvei**, **De Una**, o ambas?
  ⚠️ El componente que usa el bot es de **Jelou y solo funciona en WhatsApp** — en la web no sirve.
- **Credenciales de comercio para integración WEB** (las del bot son `LAARCOURIER-JELOU-EC`, de Jelou).
- **Ambiente de pruebas / sandbox de pago**, para desarrollar sin cobrar de verdad.
- ¿3DS obligatorio? ¿Qué método (redirección, formulario embebido)?

### 2. Dónde corre la parte servidor
Crear guías, agendar recolecciones y confirmar pagos **no puede hacerse desde el navegador**: expondría el
token de LAAR a cualquiera que abra el código de la página.
- **Opción A (recomendada):** corre en **su backend** (fenix ya tiene Node y sirve `api/ciudades`).
  Nosotros entregamos el código; ellos lo despliegan.
- **Opción B:** corre en **nuestra función** (Jelou Functions) → necesitamos **credenciales de producción
  de la API de LAAR** autorizadas para eso.

### 3. Credenciales de la API de LAAR
- Usuario/clave para **producción** (hoy usamos `whatsappuio.uio`; ¿el mismo o uno propio para la web?).
- Confirmar el ambiente de pruebas `:9752` para desarrollo (ya probado, funciona).

---

## 🟡 NECESARIO ANTES DE PUBLICAR

### 4. Espacio y URL
- ¿Ruta dentro de su sitio (`/enviafacil`) o subdominio?
- ¿Página completa o embebida en su plantilla?
- ¿Qué versión de su web (CMS, framework) para que el estilo no choque?

### 5. Permisos de red (CSP)
La página llamará a servicios nuestros. Igual que en los formularios, hay que **permitir esos dominios**
en `connect-src`. ⚠️ **Sigue pendiente `enviafacil-formlock.fn.jelou.ai` desde hace días** — conviene
resolver el criterio de una vez (p. ej. permitir `*.fn.jelou.ai`).

### 6. Monitoreo
- Su cadena de **Application Insights**, como en los formularios (va como marcador `__AI_CONNECTION_STRING__`).

### 7. Marca
- **Logo, colores y tipografía** oficiales, para que la página se vea de LAAR y no genérica.

### 8. Legales
- Enlaces vigentes de **Términos y Condiciones** y **Protección de Datos**.
- ¿La web debe pedir aceptación explícita, como el PDP del bot?

### 9. Facturación
- ¿La factura se emite igual que en el bot (`generarFactura`)?
- ¿Qué datos fiscales hay que pedir en la web (cédula/RUC, razón social, dirección)?

---

## ✅ Lo que YA tenemos y no hay que pedir
- Formulario multidestino completo (remitente → N destinos → resumen), aprobado por JC.
- Cotización de uno y varios destinos — **probada contra la API real**.
- Guías individuales + **una recolección con `nroGuia[]`** — **probada end-to-end en `:9752`**
  (2 destinos mixtos → `CONTLC50516085` + `CONTLC50516086` → `REC2028591`).
- Catálogos de ciudades y oficinas, validaciones de cédula/RUC, mapa con geocodificación.
- Documentación oficial de su API (PDF unificado).
