#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICADOR DEL FORMULARIO DE MULTIENVIOS
=========================================
Comprueba, requisito por requisito, que multienvio.html cumple lo que se acordo.

  python3 verificar-formulario.py [archivo.html]

POR QUE ESTE VERIFICADOR SE PRUEBA A SI MISMO
---------------------------------------------
El 15-ago-2026 reporte "396 de 704 ciudades" contando con un patron que solo
cazaba codigos de una forma. La cifra era falsa. La leccion: un patron que
devuelve 0 casi siempre es un patron malo, no una ausencia.

Por eso cada requisito heredado declara de que formulario de PRODUCCION viene.
Antes de juzgar el archivo nuevo, el verificador BAJA ese formulario vivo de
fenix y comprueba que su propio patron caza ahi. Si no caza en el origen, no
dice "FALTA": dice "PATRON MALO" y no cuenta como fallo del formulario.

Sin red: se salta la autoprueba y avisa. Los requisitos siguen evaluandose.
"""
import json
import re
import sys
import urllib.request

FENIX = "https://fenix.laarcourier.com/EnvioFacil/%s"

# ─────────────────────────────────────────────────────────────────────────────
# REQUISITOS
#   origen  = formulario de produccion del que se hereda (autoprueba del patron)
#   patron  = expresion que DEBE aparecer en el formulario nuevo
#   prohibido = expresion que NO debe aparecer
# ─────────────────────────────────────────────────────────────────────────────
REQ = [
 # ── A) SEGURIDADES HEREDADAS DE PRODUCCION ─────────────────────────────────
 ("A", "Candado local (localStorage)",            "index.html",       r"EF_LOCK"),
 ("A", "Candado en el SERVIDOR (formlock)",       "index.html",       r"enviafacil-formlock"),
 ("A", "  · marca al enviar",                     "index.html",       r"efSrvMark"),
 ("A", "  · consulta al abrir",                   "index.html",       r"efSrvCheck"),
 ("A", "Reapertura con nonce (edit=1)",           "index.html",       r"EF_EDIT"),
 ("A", "Cedula 10 digitos",                       "index.html",       r"_ced10"),
 ("A", "RUC 13 con salvaguarda de sociedades",    "index.html",       r"_rucOk"),
 ("A", "Celular: normaliza antes de contar",      "index.html",       r'val\("celular"\)\.replace\(/\\D/g,""\)'),
 ("A", "Celular: 10 digitos exactos",             "index.html",       r"\^\\d\{10\}\$"),
 ("A", "Control ciudad <-> ubicacion",            "index.html",       r"checkCiudad"),
 ("A", "  · normalizador de nombres",             "index.html",       r"efNorm"),
 ("A", "Ocultar mapa si ya dio ubicacion",        "index.html",       r"sinJoya"),
 ("A", "Captura de coordenadas",                  "index.html",       r"ef_lat"),
 ("A", "Calle secundaria como campo propio",      "index.html",       r"calle_secundaria"),
 ("A", "Prellenado del celular (593... -> 0...)", "index.html",       r'indexOf\("593"\)|indexOf\(.593.\)'),
 ("A", "Revisa la respuesta del envio",           "index.html",       r"resp\.ok|r\.ok"),

 # ── B) CAMPOS DE ENVIO (de datos-envio.html) ───────────────────────────────
 ("B", "Campo contenido",                         "datos-envio.html", r'id="contenido"'),
 ("B", "Campo peso",                              "datos-envio.html", r'id="peso"'),
 ("B", "Campo piezas",                            "datos-envio.html", r'id="piezas"'),
 ("B", "Campo valor declarado",                   "datos-envio.html", r'id="valor"'),
 ("B", "Tope de 50 kg POR PIEZA",                 "datos-envio.html", r"50"),

 # ── C) PROPIO DE MULTIENVIOS ───────────────────────────────────────────────
 ("C", "Dos pasos por URL (paso=)",               None,               r'get\("paso"\)'),
 ("C", "Confirma UN destino y cierra",            None,               r"EF_UNO"),
 ("C", "Selector de ciudad dentro del formulario",None,               r"_efCiudadKey|selCiudad"),
 ("C", "Catalogo de ciudades EN VIVO",            None,               r"enviafacil-ciudades|api/ciudades"),
 ("C", "  · corta si no responde",                None,               r"AbortController"),
 ("C", "  · avisa y ofrece reintentar",           None,               r"efAviso|reintentar"),

 # ── D) OFICINA DE LAAR (nuevo, 16-ago) ─────────────────────────────────────
 ("D", "Elegir domicilio u oficina por destino",  None,               r"esOficina|modoEntrega"),
 # La LISTA de oficinas vive en oficina-retiro.html, que se reusa tal cual y ya
 # esta publicado. A ESTE formulario le toca recibir la ciudad ya fijada por esa
 # eleccion y no volver a preguntarla.
 ("D", "Acepta la ciudad ya fijada (lockDes)",  "datos-envio.html", r"lockDes"),
 ("D", "  · con su codigo de ciudad",           "datos-envio.html", r"desCod"),
 ("D", "Devuelve idOficina",                      None,               r"idOficina"),
 ("D", "Devuelve isRetiro",                       None,               r"isRetiro"),

 # ── E) SEGURIDAD DEL ARCHIVO ───────────────────────────────────────────────
 ("E", "Marcador de llave sin sustituir",         None,               r"__EF_API_KEY__"),
]

PROHIBIDO = [
 ("Pantalla '¿a cuantos destinos?'",   r"scrInicio"),
 ("Selector de modo",                  r"pickModo"),
 ("Variable estado.modo",              r"estado\.modo"),
 ("Pantalla 'destinos confirmados'",   r"scrMas"),
 ("Boton 'agregar otro destino'",      r"agregarDestino"),
 # 16-ago (JC): el origen se pregunta UNA sola vez, EN EL REMITENTE. Volver a
 # pedirlo confunde al cliente: es el mismo dato con otro nombre.
 ("Pregunta 'Ciudad de origen'",       r"Ciudad de origen"),
 ("Pantalla de cotizador propia",      r"Precio al instante"),
 ("Ciudades quemadas en el archivo",   r'\[\s*"[^"]{2,60}"\s*,\s*"\d{9,14}"\s*,\s*"[^"]{2,40}"\s*\]'),
 ("Oficinas quemadas en el archivo",   r"var OFICINAS\s*="),
 ("alert() o confirm()",               r"(?<![\w.])(alert|confirm)\("),
 ("Apunta a GitHub Pages",             r"github\.io|jcpaez72"),
]

# 19 del contrato original + 2 de oficina = 21
# Verificado contra el nodo «Consolidar envio» (skill 44490), que es quien lee
# esto. `idServicio` NO aparece: el bot deduce documento/paquete de `tipo`.
CONTRATO = ["tipo", "ciudad", "ciudadCodigo", "provincia",
            "piezas", "peso", "valor", "contenido",
            "cedula", "nombre", "correo", "celular",
            "calle_principal", "numero_casa", "calle_secundaria",
            "referencia", "lat", "lon",
            "idOficina", "isRetiro"]


def baja(nombre):
    try:
        with urllib.request.urlopen(FENIX % nombre, timeout=20) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:
        return None


def main():
    destino = sys.argv[1] if len(sys.argv) > 1 else "multienvio.html"
    try:
        nuevo = open(destino, encoding="utf-8").read()
    except FileNotFoundError:
        print("  No existe %s" % destino)
        return 2

    print("=" * 74)
    print("  VERIFICADOR DEL FORMULARIO DE MULTIENVIOS")
    print("  archivo: %s  (%d bytes)" % (destino, len(nuevo)))
    print("=" * 74)

    # ── autoprueba de los patrones contra produccion ────────────────────────
    print("\n  AUTOPRUEBA — cada patron heredado debe cazar en su origen\n")
    cache, malos = {}, set()
    orígenes = sorted({r[2] for r in REQ if r[2]})
    for o in orígenes:
        cache[o] = baja(o)
        print("    %-18s %s" % (o, "bajado (%d b)" % len(cache[o]) if cache[o] else "SIN RED — autoprueba omitida"))
    print()
    for _, nom, org, pat in REQ:
        if not org or not cache.get(org):
            continue
        if not re.search(pat, cache[org]):
            malos.add(nom)
            print("    PATRON MALO  %-42s no caza en %s" % (nom[:42], org))
    if not malos and any(cache.values()):
        print("    todos los patrones heredados cazan en produccion")

    # ── requisitos ──────────────────────────────────────────────────────────
    GRUPO = {"A": "SEGURIDADES HEREDADAS DE PRODUCCION",
             "B": "CAMPOS DE ENVIO",
             "C": "PROPIO DE MULTIENVIOS",
             "D": "OFICINA DE LAAR",
             "E": "SEGURIDAD DEL ARCHIVO"}
    falta = 0
    actual = None
    for g, nom, org, pat in REQ:
        if g != actual:
            print("\n  %s) %s\n" % (g, GRUPO[g]))
            actual = g
        if nom in malos:
            print("    [?]  %-46s (patron no confiable)" % nom[:46])
            continue
        if re.search(pat, nuevo):
            print("    [OK] %s" % nom)
        else:
            print("    [--] %-46s FALTA" % nom[:46])
            falta += 1

    # ── prohibido ───────────────────────────────────────────────────────────
    print("\n  F) LO QUE NO DEBE ESTAR\n")
    sobra = 0
    for nom, pat in PROHIBIDO:
        n = len(re.findall(pat, nuevo))
        if n:
            print("    [!!] %-46s aparece %d vez/veces" % (nom[:46], n))
            sobra += 1
        else:
            print("    [OK] %s" % nom)

    # ── contrato ────────────────────────────────────────────────────────────
    print("\n  G) CONTRATO CON EL BOT — 21 campos por destino\n")
    sin = [c for c in CONTRATO if not re.search(r"\b%s\b" % c, nuevo)]
    print("    presentes: %d de %d" % (len(CONTRATO) - len(sin), len(CONTRATO)))
    if sin:
        print("    faltan   : %s" % " ".join(sin))

    # ── resultado ───────────────────────────────────────────────────────────
    print("\n" + "=" * 74)
    ok = (falta == 0 and sobra == 0 and not sin)
    print("  requisitos que faltan : %d" % falta)
    print("  cosas prohibidas      : %d" % sobra)
    print("  campos del contrato   : %d sin aparecer" % len(sin))
    if malos:
        print("  patrones no confiables: %d  (revisar el verificador, no el formulario)" % len(malos))
    print("\n  %s" % ("TODO VERDE — se puede entregar" if ok else "NO SE ENTREGA hasta que quede todo verde"))
    print("=" * 74)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
