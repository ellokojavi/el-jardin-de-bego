#!/usr/bin/env python3
"""Busca y descarga imágenes de Wikimedia Commons para las guías.

Uso:
  python3 scripts/imagenes.py buscar "carabela replica"      # lista candidatas
  python3 scripts/imagenes.py bajar "File:X.jpg" nombre-salida

Las imágenes quedan en imagenes/ y los créditos se acumulan en
imagenes/creditos.json, que es lo que alimenta el pie de cada foto.
"""
import json, re, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "imagenes"
CREDITOS = DESTINO / "creditos.json"
UA = {"User-Agent": "JardinDeBego/1.0 (material escolar; https://github.com/ellokojavi/el-jardin-de-bego)"}
API = "https://commons.wikimedia.org/w/api.php"


_ultima = [0.0]


def api(p, intentos=4):
    """Llama a la API respetando un ritmo suave: Commons responde 429 si uno insiste."""
    p.update({"format": "json", "formatversion": "2"})
    url = API + "?" + urllib.parse.urlencode(p)
    espera = 3.0
    for i in range(intentos):
        pausa = 1.5 - (time.time() - _ultima[0])
        if pausa > 0:
            time.sleep(pausa)
        _ultima[0] = time.time()
        try:
            r = urllib.request.Request(url, headers=UA)
            return json.load(urllib.request.urlopen(r, timeout=40))
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == intentos - 1:
                raise
            time.sleep(espera)
            espera *= 2


def limpio(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", s).strip()


def buscar(consulta, n=8, ancho=900):
    d = api({"action": "query", "generator": "search",
             "gsrsearch": f"{consulta} filetype:bitmap", "gsrnamespace": "6",
             "gsrlimit": str(n), "prop": "imageinfo",
             "iiprop": "url|extmetadata|size|mime", "iiurlwidth": str(ancho)})
    salida = []
    for p in d.get("query", {}).get("pages", []):
        ii = p.get("imageinfo", [{}])[0]
        if ii.get("mime") not in ("image/jpeg", "image/png"):
            continue
        em = ii.get("extmetadata", {})
        salida.append({
            "titulo": p["title"],
            "licencia": em.get("LicenseShortName", {}).get("value", "?"),
            "autor": limpio(em.get("Artist", {}).get("value"))[:70],
            "px": f'{ii.get("width")}x{ii.get("height")}',
            "thumb": ii.get("thumburl", ""),
            "pagina": ii.get("descriptionurl", ""),
        })
    return salida


def bajar(titulo, nombre, ancho=900):
    d = api({"action": "query", "titles": titulo, "prop": "imageinfo",
             "iiprop": "url|extmetadata|mime", "iiurlwidth": str(ancho)})
    pag = d["query"]["pages"][0]
    ii = pag["imageinfo"][0]
    em = ii.get("extmetadata", {})
    datos = urllib.request.urlopen(
        urllib.request.Request(ii["thumburl"], headers=UA), timeout=60).read()

    DESTINO.mkdir(exist_ok=True)
    ext = ".png" if ii.get("mime") == "image/png" else ".jpg"
    ruta = DESTINO / (nombre + ext)
    ruta.write_bytes(datos)

    # recomprimir para que el repositorio no engorde
    try:
        from PIL import Image
        im = Image.open(ruta)
        if ext == ".jpg":
            im.convert("RGB").save(ruta, "JPEG", quality=82, optimize=True, progressive=True)
        else:
            im.save(ruta, "PNG", optimize=True)
    except Exception as e:
        print("  (sin recomprimir:", e, ")")

    creditos = json.loads(CREDITOS.read_text(encoding="utf-8")) if CREDITOS.exists() else {}
    creditos[ruta.name] = {
        "titulo": pag["title"],
        "autor": limpio(em.get("Artist", {}).get("value")) or "autor desconocido",
        "licencia": em.get("LicenseShortName", {}).get("value", "?"),
        "pagina": ii.get("descriptionurl", ""),
    }
    CREDITOS.write_text(json.dumps(creditos, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"→ {ruta.name}  {ruta.stat().st_size // 1024} KB  · {creditos[ruta.name]['licencia']}")
    return ruta


if __name__ == "__main__":
    if sys.argv[1] == "buscar":
        for r in buscar(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 8):
            print(f'· {r["titulo"][5:78]}\n    {r["licencia"]:16} {r["px"]:12} {r["autor"][:46]}')
    elif sys.argv[1] == "bajar":
        bajar(sys.argv[2], sys.argv[3])
