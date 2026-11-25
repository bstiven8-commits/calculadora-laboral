#!/usr/bin/env python3
"""
Generador del sitio de la Calculadora Laboral (v2: contenido de alto valor).

Crea páginas HTML independientes, listas para subir al hosting:
  - 12 guías largas (horas extra, indemnización, PILA, liquidación, cesantías, prima,
    vacaciones, salario mínimo, costo de un empleado, contratista vs empleado,
    calendario de obligaciones y glosario)
  - blog.html, sobre-nosotros.html, contacto.html, privacidad.html, terminos.html
  - sitemap.xml y robots.txt

Uso (una sola vez, antes de ejecutar, escribe tu correo real de contacto):
    CORREO=tucorreo@gmail.com python3 generar_sitio.py
o edita la constante CORREO aquí abajo. NO se sobrescribe index.html ni ads.txt.

Para cambiar tarifas del año: edita S, AUX y los parámetros de la sección "CIFRAS".
Para editar un texto: busca el artículo en la lista ARTICULOS (cada uno es un diccionario).
"""
import os, sys, math, re, json, datetime, html

# ====== CONFIGURACIÓN ======
DOMINIO = "calculadoralaboralcolombia.online"      # sin https:// ni barra final
SALIDA = "sitio"                                    # carpeta donde se escriben los archivos
CORREO = os.environ.get("CORREO", "")               # correo público de contacto (obligatorio)
MARCA = "Calculadora Laboral Colombia"
ADS_CLIENT = "ca-pub-3761150056608968"
GA_ID = os.environ.get("GA_ID", "GTM-MPSK8MKB")   # etiqueta de Google (GTM-… o G-…); vacío = sin analítica
ACTUALIZADO = "noviembre de 2026"
REVISADO = "25 de noviembre de 2026"                # fecha de la última revisión de cifras y normas (actualízala al revisar)
# ===========================

if not CORREO or "@" not in CORREO:
    sys.exit("Falta el correo de contacto. Ejecuta:  CORREO=tucorreo@dominio.com python3 generar_sitio.py")

HOY = datetime.date.today().isoformat()

# ====== CIFRAS 2026 (Decretos 1469 y 1470 de 2025) ======
S = 1750905            # SMMLV
AUX = 249095           # auxilio de transporte
f = lambda n: "$ " + f"{round(n):,}".replace(",", ".")
pc = lambda x: f"{x:.1f}".replace(".", ",").rstrip("0").rstrip(",") if isinstance(x, float) else str(x)
up = lambda x: math.ceil(round(x / 100, 6)) * 100          # redondeo PILA al múltiplo de $100 hacia arriba
SAL = 3_500_000                                             # salario de ejemplo (menor a 2 SMMLV: recibe auxilio)
HORA = SAL / 210                                            # jornada de 42 h: 42 x 30 / 6 = 210 horas al mes


def pila(ingresos, costos=0, arl=0.00522, caja=0.0):
    """Planilla de un independiente. Devuelve dict con cada aporte."""
    ibcb = (ingresos - costos) * .4
    ibc = round(min(max(ibcb, S), 25 * S))
    fsp_r = fsp_rate(ibc)
    d = dict(ibc=ibc, salud=up(ibc * .125), pension=up(ibc * .16), fsp=up(ibc * fsp_r), fsp_r=fsp_r,
             arl=up(ibc * arl), caja=up(ibc * caja) if caja else 0)
    d["total"] = d["salud"] + d["pension"] + d["fsp"] + d["arl"] + d["caja"]
    return d


def fsp_rate(ibc):
    m = ibc / S
    if m < 4: return 0
    if m < 16: return .01
    if m < 17: return .012
    if m < 18: return .014
    if m < 19: return .016
    if m < 20: return .018
    return .02


# ====== PLANTILLA ======
TPL = r'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>@TITLE@</title>
<meta name="description" content="@DESC@">
<link rel="canonical" href="https://@DOM@/@FILE@">
<meta property="og:type" content="article"><meta property="og:title" content="@TITLE@"><meta property="og:description" content="@DESC@"><meta property="og:url" content="https://@DOM@/@FILE@"><meta property="og:locale" content="es_CO">
<meta name="theme-color" content="#101B3B">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧮</text></svg>">
@ADS@
@GA@
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Spline+Sans+Mono:wght@400..700&display=swap">
@JSONLD@
<style>
:root{--bg:#E5EDE2;--surface:#FAFBF7;--ink:#101B3B;--muted:#4F5B73;--line:#C3D0BE;--accent:#1B45C9;--accent-ink:#fff;--soft:#DCE5FA;--mark:#F5D547;--warn:#7A4A00;--warn-soft:#F6E7B8;--on-ink:#FAFBF7;--sans:"Archivo",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"Spline Sans Mono",ui-monospace,Menlo,monospace;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--bg:#0D1424;--surface:#151E33;--ink:#E8ECF7;--muted:#9AA6C2;--line:#2A3552;--accent:#8FA8FF;--accent-ink:#0D1424;--soft:#1E2B52;--mark:#E7C94A;--warn:#F2C060;--warn-soft:#33270D;--on-ink:#0D1424;color-scheme:dark}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 var(--sans);padding:env(safe-area-inset-top) 0 env(safe-area-inset-bottom)}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
header{border-bottom:1px solid var(--line);background:var(--surface)}
.in{max-width:46rem;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left))}
header .in{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding-top:.7rem;padding-bottom:.7rem;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:.6rem;font:800 1.05rem var(--sans);font-stretch:112%;color:var(--ink);text-decoration:none}
.brand i{width:2rem;height:2rem;border-radius:5px;background:var(--ink);color:var(--on-ink);display:grid;place-items:center;font:600 .8rem var(--mono);font-style:normal}
nav{display:flex;align-items:center;gap:1rem;flex-wrap:wrap}
nav a:not(.btn){text-decoration:none;color:var(--muted);font-size:.93rem}nav a:not(.btn):hover{color:var(--accent);text-decoration:underline}
.btn{display:inline-block;padding:.65rem 1.15rem;border-radius:6px;background:var(--accent);color:var(--accent-ink);font-weight:700;text-decoration:none}
.btn.s{padding:.4rem .8rem;font-size:.88rem}
h1{font:800 clamp(1.9rem,6vw,2.8rem)/1.06 var(--sans);font-stretch:116%;letter-spacing:-.018em;margin:.5rem 0 .7rem;text-wrap:balance}
h2{font:800 1.5rem/1.2 var(--sans);font-stretch:108%;letter-spacing:-.01em;margin:2.4rem 0 .5rem;scroll-margin-top:1rem;padding-top:1.1rem;border-top:2px solid var(--ink)}
h3{font-size:1.05rem;font-weight:700;margin:1.4rem 0 .2rem}
p,li{max-width:66ch}p{margin:.6rem 0 1rem}li{margin:.3rem 0}
.meta{color:var(--muted);font-size:.9rem}
a{color:var(--accent);text-underline-offset:3px}
.lead{font-size:1.15rem;line-height:1.6}
.box,.slip{position:relative;background:var(--surface);border:1px solid var(--line);border-bottom:0;border-radius:6px 6px 0 0;padding:1.1rem 1.3rem 1.7rem;margin:1.5rem 0}
.box::after,.slip::after{content:"";position:absolute;left:0;right:0;bottom:0;height:10px;background:radial-gradient(circle at 8px 10px,var(--bg) 5px,transparent 5.5px) 0 0/16px 10px repeat-x}
.box p{margin:.3rem 0}.box ul{margin:.4rem 0 .2rem;padding-left:1.2rem}
.box>p:first-child b{font-weight:800}
.warn{border-left:5px solid var(--warn);background:var(--warn-soft)}
.toc{background:transparent;border:0;border-left:3px solid var(--ink);padding:.2rem 0 .2rem 1rem;margin:1.6rem 0;font-size:.95rem}
.toc b{display:block;margin-bottom:.2rem}.toc ol{margin:.2rem 0;padding-left:1.2rem}
.cta{background:var(--ink);color:var(--on-ink);border-radius:6px;padding:1.4rem 1.3rem;margin:2.4rem 0}
.cta p{margin:0 0 .8rem}.cta .btn{background:var(--mark);color:#101B3B}
.card{display:block;background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--ink);border-radius:4px;padding:.9rem 1.1rem;margin:.7rem 0;text-decoration:none;color:var(--ink)}
.card:hover{border-left-color:var(--accent);background:var(--soft)}.card small{color:var(--accent);font-weight:700}.card b{display:block;font-size:1.05rem}.card span{color:var(--muted);font-size:.92rem}
table{border-collapse:collapse;width:100%;font-size:.95rem;margin:.6rem 0}
th{font-weight:700;color:var(--muted);font-size:.86rem;border-bottom:2px solid var(--ink)}
th,td{padding:.5rem .5rem;text-align:left;vertical-align:top}
td{border-bottom:1px dotted color-mix(in srgb,var(--ink) 45%,transparent)}
td.n,th.n{text-align:right;white-space:nowrap;font-family:var(--mono);font-variant-numeric:tabular-nums}
tr:has(td>b:only-child) td{background:linear-gradient(transparent 62%,color-mix(in srgb,var(--mark) 70%,transparent) 62%)}
.tw{overflow-x:auto;margin:.6rem 0 1rem}
.fuentes li{font-size:.93rem}
footer{background:var(--ink);color:var(--on-ink);margin-top:3.5rem;padding:1.6rem 0 2.4rem;font-size:.88rem}
footer .cols{display:flex;gap:2.5rem;flex-wrap:wrap}footer .cols div{min-width:11rem}
footer a{display:block;margin:.3rem 0;color:var(--on-ink);opacity:.8;text-decoration:none}footer a:hover{opacity:1;text-decoration:underline}
footer b{color:var(--on-ink)}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
</style></head><body>
<header><div class="in"><a class="brand" href="index.html"><i aria-hidden="true">=$</i>@MARCA@</a><nav><a href="index.html#inicio">Inicio</a><a href="blog.html">Guías</a><a href="sobre-nosotros.html">Sobre el sitio</a><a class="btn s" href="@CALC@">Calculadora</a></nav></div></header>
<main class="in"><article>
<p class="meta" style="margin-top:1.2rem"><a href="index.html#inicio">Inicio</a> › <a href="blog.html">Guías</a> › @TAG@</p>
<h1>@H1@</h1>
@METALINE@
@RESUMEN@
@TOC@
@BODY@
@FAQ@
@FUENTES@
@CTA@
@MORE@
@DISC@
</article></main>
<footer><div class="in"><div class="cols">
<div><b>Guías</b>@FOOTGUIAS@</div>
<div><b>El sitio</b><a href="index.html">Calculadora</a><a href="blog.html">Todas las guías</a><a href="sobre-nosotros.html">Sobre el sitio y metodología</a><a href="contacto.html">Contacto</a><a href="privacidad.html">Política de privacidad</a><a href="terminos.html">Términos y descargo</a></div>
</div><p style="margin-top:1.2rem">© 2026 @MARCA@. Contenido informativo, no constituye asesoría jurídica.</p></div></footer>
</body></html>'''

ADS = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADS_CLIENT}" crossorigin="anonymous"></script>'

if GA_ID.startswith("GTM-"):      # fragmento tal como lo entrega Google al instalar manualmente la etiqueta
    GA = (f'<script async src="https://www.googletagmanager.com/gtm.js?id={GA_ID}"></script>'
          '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());</script>')
elif GA_ID:
    GA = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
          f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA_ID}");</script>')
else:
    GA = ""
ANALITICA = ('<h2>Analítica de visitas (Google Analytics)</h2>'
             '<p>Usamos Google Analytics para conocer, de forma agregada, qué páginas se visitan, desde qué países o dispositivos y desde qué enlaces llegan los visitantes. Google Analytics usa cookies y recibe información técnica de tu navegador. Los datos se usan solo con fines estadísticos y para mejorar las guías. Los valores que escribes en la calculadora no se envían a Google Analytics. '
             'Puedes impedir la medición con el <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener" target="_blank">complemento de inhabilitación de Google Analytics</a> o bloqueando las cookies en tu navegador.</p>') if GA_ID else ""

# ====== utilidades de contenido ======
def tabla(cabeceras, filas, numericas=()):
    """cabeceras: lista de str; filas: lista de listas; numericas: índices de columnas alineadas a la derecha"""
    th = "".join(f'<th class="n">{h}</th>' if i in numericas else f"<th>{h}</th>" for i, h in enumerate(cabeceras))
    tr = "".join("<tr>" + "".join(f'<td class="n">{c}</td>' if i in numericas else f"<td>{c}</td>" for i, c in enumerate(r)) + "</tr>" for r in filas)
    return f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def slug(t):
    t = re.sub(r"<[^>]+>", "", t).lower()
    for a, b in zip("áéíóúñü", "aeiounu"): t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def prep(body):
    """Añade id a cada <h2> y devuelve (body, toc_html)."""
    items = []
    def r(m):
        t = m.group(1); i = slug(t); items.append((i, re.sub(r"<[^>]+>", "", t)))
        return f'<h2 id="{i}">{t}</h2>'
    body = re.sub(r"<h2>(.*?)</h2>", r, body)
    toc = ""
    if len(items) >= 4:
        toc = '<div class="toc" role="navigation" aria-label="Contenido"><b>En esta guía</b><ol>' + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items) + "</ol></div>"
    return body, toc


def faq_html(faq):
    if not faq: return "", ""
    h = "<h2>Preguntas frecuentes</h2>" + "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faq)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": re.sub(r"<[^>]+>", "", q), "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faq]}
    return h, ld


def fuentes_html(fu):
    if not fu: return ""
    li = "".join(f'<li>{t if not u else f"""<a href="{u}" rel="noopener" target="_blank">{t}</a>"""}</li>' for t, u in fu)
    return f'<h2 id="fuentes">Normas y fuentes de referencia</h2><ul class="fuentes">{li}</ul><p class="meta">Las normas pueden cambiar: confirma su vigencia en el Gestor Normativo de la Función Pública o en la entidad competente.</p>'


# enlaces oficiales (solo dominios raíz verificables)
F_CST = ("Código Sustantivo del Trabajo, texto oficial (Secretaría del Senado)", "https://www.secretariasenado.gov.co/senado/basedoc/codigo_sustantivo_trabajo.html")
F_GN = ("Gestor Normativo de la Función Pública (leyes y decretos vigentes)", "https://www.funcionpublica.gov.co/eva/gestornormativo/")
F_MT = ("Ministerio del Trabajo", "https://www.mintrabajo.gov.co/")
F_UGPP = ("UGPP, Unidad de Gestión Pensional y Parafiscales", "https://www.ugpp.gov.co/")

# ==========================================================================================
# ARTÍCULOS
# ==========================================================================================
ARTICULOS = []

# ------------------------------------------------------------------ HORAS EXTRA
fac = [("Hora extra diurna", .25), ("Hora extra nocturna", .75), ("Recargo nocturno (hora ordinaria de noche)", .35),
       ("Dominical o festivo diurno", .90), ("Nocturno en dominical o festivo", 1.25),
       ("Extra diurna en dominical o festivo", 1.15), ("Extra nocturna en dominical o festivo", 1.65)]
tabh = tabla(["Tipo de hora", "Recargo", "Factor", "Valor de la hora"],
             [[a, f"{round(b*100)}%", pc(round(1 + b, 2)).replace(".", ","), f(HORA * (1 + b))] for a, b in fac], numericas=(1, 2, 3))
tabdiv = tabla(["Periodo", "Horas semanales", "Divisor mensual"],
               [["15 jul 2023 – 14 jul 2024", "47", "235"], ["15 jul 2024 – 14 jul 2025", "46", "230"],
                ["15 jul 2025 – 14 jul 2026", "44", "220"], ["Desde el 15 jul 2026", "42", "210"]], numericas=(1, 2))
h_edd = 10 * HORA * 1.25; h_end = 4 * HORA * 1.75; h_noc = 12 * HORA * .35; h_dom = 8 * HORA * 1.90
h_tot = h_edd + h_end + h_noc + h_dom

HEX = f'''<p class="lead">Las horas extra, los recargos nocturnos y el trabajo en domingos y festivos son de los rubros que más errores tienen en los desprendibles de pago. En 2026 cambiaron tres cosas a la vez: la jornada baja a 42 horas, la noche empieza a las 7 p. m. y el recargo dominical sube al 90%. Esta guía te muestra cómo calcular cada hora, paso a paso y con un mes completo de ejemplo.</p>
<h2>Qué cambió en 2026</h2>
<ul>
<li><b>Jornada de 42 horas semanales.</b> La Ley 2101 de 2021 redujo la jornada por etapas y la última comenzó el 15 de julio de 2026. Esto cambia el divisor con el que se calcula el valor de la hora.</li>
<li><b>La jornada nocturna empieza a las 7 p. m.</b> La reforma laboral (Ley 2466 de 2025) adelantó el inicio del trabajo nocturno: ahora va de 7 p. m. a 6 a. m. Muchas guías antiguas todavía dicen 9 p. m.</li>
<li><b>Recargo dominical y festivo del 90%.</b> La reforma lo sube de forma gradual: 80% desde julio de 2025, 90% desde el 1 de julio de 2026 y 100% desde el 1 de julio de 2027. Si ves 75% en un artículo, es la cifra anterior a la reforma.</li>
</ul>
<h2>Paso 1: el valor de la hora ordinaria</h2>
<p>La hora ordinaria se obtiene dividiendo el salario mensual entre las horas ordinarias del mes. Se calcula así: horas semanales × 30 días ÷ 6 días laborales a la semana. Con 42 horas, el divisor es <b>210</b> (42 × 30 ÷ 6). El divisor fue cambiando con la reducción de la jornada:</p>
{tabdiv}
<p>Con un salario de {f(SAL)}, la hora ordinaria vale {f(SAL)} ÷ 210 = <b>{f(HORA)}</b>. Si en tu desprendible el valor de la hora sale distinto, mira primero qué divisor usó tu empresa: es el error más común. Si tu contrato pacta una jornada menor a la legal, el divisor se calcula con tus horas reales.</p>
<h2>Paso 2: identifica el tipo de hora</h2>
<ul>
<li><b>Hora extra diurna:</b> la que excede la jornada máxima y se trabaja entre las 6 a. m. y las 7 p. m. Recargo del 25%.</li>
<li><b>Hora extra nocturna:</b> la que excede la jornada y se trabaja entre las 7 p. m. y las 6 a. m. Recargo del 75%.</li>
<li><b>Recargo nocturno:</b> hora ordinaria (dentro de tu jornada) trabajada de noche. Recargo del 35%.</li>
<li><b>Dominical o festivo:</b> trabajo en día de descanso obligatorio. Recargo del 90% en 2026.</li>
</ul>
<p>Los recargos se suman cuando coinciden. Una hora extra nocturna un domingo suma 75% + 90% = 165% de recargo. La tabla muestra el valor de cada hora para un salario de {f(SAL)}:</p>
{tabh}
<p class="meta">Factor = 1 + recargo. Valor de la hora = valor de la hora ordinaria × factor.</p>
<h2>Paso 3: cómo se suma cada hora a tu salario</h2>
<p>Aquí está la parte que más confunde. El factor de la tabla es el valor total de la hora, pero no siempre se suma completo a tu sueldo:</p>
<ul>
<li><b>Horas extra:</b> no están dentro de tu salario mensual, así que se pagan completas (factor 1,25 o 1,75).</li>
<li><b>Recargo nocturno:</b> la hora ordinaria ya está pagada en tu salario. Solo se suma el recargo del 35%.</li>
<li><b>Dominical o festivo ocasional:</b> si descansas los domingos y un domingo te piden trabajar, esas horas no estaban dentro de tu salario ordinario. Se pagan con el valor de la hora más el recargo (factor 1,90 en 2026).</li>
<li><b>Dominical o festivo habitual:</b> si trabajas domingos como parte de tu jornada semanal normal y descansas otro día, la hora ya está en tu salario y se suma solo el recargo (0,90).</li>
</ul>
<div class="box warn"><p><b>Ojo con la interpretación.</b> Sobre el trabajo dominical hay conceptos del Ministerio del Trabajo y sentencias que matizan estos casos según cómo esté pactado el descanso. Si tu empresa te paga distinto, no asumas que está mal ni bien: pide el soporte del cálculo y, si persiste la duda, consulta con el Ministerio del Trabajo. La calculadora de este sitio aplica el caso habitual (solo el recargo en dominicales).</p></div>
<h2>Ejemplo completo: un mes con varios tipos de hora</h2>
<p>Una persona con salario de {f(SAL)} (hora ordinaria de {f(HORA)}) trabajó este mes:</p>
{tabla(["Concepto", "Cálculo", "Valor"], [
 ["10 horas extra diurnas", f"10 × {f(HORA*1.25)}", f(h_edd)],
 ["4 horas extra nocturnas", f"4 × {f(HORA*1.75)}", f(h_end)],
 ["12 horas ordinarias nocturnas (solo recargo)", f"12 × {f(HORA*.35)}", f(h_noc)],
 ["8 horas en un domingo ocasional, de día", f"8 × {f(HORA*1.9)}", f(h_dom)],
 ["<b>Total adicional al salario</b>", "", f"<b>{f(h_tot)}</b>"]], numericas=(2,))}
<p>Ese total se suma al salario básico. Si el desprendible de ese mes muestra una cifra muy inferior y no hay una explicación escrita, vale la pena pedir el detalle.</p>
<h2>Cómo revisar tu desprendible en cinco pasos</h2>
<ol>
<li>Confirma el divisor: con el salario del ejemplo, la hora debe valer {f(HORA)}, no {f(SAL/235)} (divisor 235 antiguo).</li>
<li>Cuenta tus horas reales: lleva un registro propio (agenda, fotos del turno, mensajes de la programación).</li>
<li>Clasifica cada hora (diurna, nocturna, dominical, festiva) con los horarios de 2026: noche desde las 7 p. m.</li>
<li>Multiplica por el factor correcto y compara con la línea de tu desprendible.</li>
<li>Verifica que las horas extra estén incluidas en la base de tus aportes a seguridad social.</li>
</ol>
<h2>Límites y reglas importantes</h2>
<ul>
<li>No se pueden trabajar más de 2 horas extra al día ni más de 12 a la semana (CST, art. 163).</li>
<li>La ley exige autorización del Ministerio del Trabajo para el trabajo suplementario. Aun así, si el empleador pide las horas y las recibe, debe pagarlas.</li>
<li>Los cargos de dirección, confianza y manejo no tienen derecho a horas extra (CST, art. 162). Esto depende de las funciones reales, no del nombre del cargo.</li>
<li>Los trabajadores con salario integral no reciben recargos ni horas extra por separado, porque su salario ya las contempla.</li>
</ul>
<h2>Efecto en prestaciones y seguridad social</h2>
<p>Las horas extra y los recargos hacen parte del salario. Por eso cuentan para la base de aportes a salud y pensión, para la prima y para las cesantías. Si trabajas horas extra de forma habitual, tu salario es variable en parte: las prestaciones se calculan con el promedio. Ver la <a href="como-se-calcula-la-liquidacion.html">guía de liquidación</a>.</p>
<h2>Qué hacer si no te pagan las horas extra</h2>
<p>Primero, pide por escrito el detalle del cálculo a recursos humanos o a tu jefe. Reúne soportes: programación de turnos, registros de ingreso y salida, correos y mensajes. Si no hay respuesta, puedes acudir a la inspección de trabajo del Ministerio del Trabajo. Ten presente que las acreencias laborales prescriben en 3 años desde que se hacen exigibles (CST, art. 488), así que no conviene esperar mucho.</p>'''

ARTICULOS.append(dict(
    file="horas-extra.html", tag="Jornada laboral 2026", calc="index.html#hex",
    h1="Cómo calcular las horas extra y recargos en Colombia (2026)",
    title="Horas extra y recargos 2026 en Colombia: cómo calcularlos | Calculadora Laboral",
    desc="Guía 2026: valor de la hora con la jornada de 42 horas, recargo nocturno desde las 7 p. m., dominical al 90%, tabla de factores y un mes completo de ejemplo.",
    card="Valor de la hora con 42 horas, noche desde las 7 p. m. y dominical al 90%, con ejemplo de un mes completo.",
    resumen=["La hora ordinaria con 42 horas semanales se calcula dividiendo el salario entre 210.",
             "La noche empieza a las 7 p. m. y el recargo dominical y festivo es del 90% desde el 1 de julio de 2026.",
             "Los recargos se suman cuando coinciden, pero no todos se pagan completos: depende de si la hora ya está en tu salario."],
    body=HEX,
    faq=[("¿Cuánto vale una hora extra diurna en 2026?", f"Se paga con un recargo del 25% sobre la hora ordinaria. Con un salario de {f(SAL)}, la hora ordinaria vale {f(HORA)} y la extra diurna {f(HORA*1.25)}."),
         ("¿Desde qué hora es nocturno el trabajo?", "Desde las 7 p. m. hasta las 6 a. m., según la reforma laboral (Ley 2466 de 2025). Antes de la reforma la noche empezaba a las 9 p. m."),
         ("¿Cuál es el recargo por trabajar domingos y festivos?", "El recargo es del 90% desde el 1 de julio de 2026 y subirá al 100% el 1 de julio de 2027."),
         ("¿Cuántas horas extra se pueden trabajar?", "Máximo 2 por día y 12 por semana. Los cargos de dirección, confianza y manejo no tienen derecho a horas extra."),
         ("¿Las horas extra cuentan para la prima y las cesantías?", "Sí. Son factor salarial, por lo que se incluyen en la base de la prima, las cesantías y los aportes a seguridad social.")],
    fuentes=[("Código Sustantivo del Trabajo, arts. 159 a 168 y 179 a 180", None), ("Ley 2101 de 2021 (reducción gradual de la jornada a 42 horas)", None),
             ("Ley 2466 de 2025 (reforma laboral: jornada nocturna y recargo dominical gradual)", None), F_CST, F_MT, F_GN]))

# ------------------------------------------------------------------ INDEMNIZACIÓN
def dias_ind(anios, alto=False):
    p, a = (20, 15) if alto else (30, 20)
    return p if anios <= 1 else p + a * (anios - 1)

DIA = SAL / 30
filas_ind = [[t, str(dias_ind(y)), f(DIA * dias_ind(y)), str(dias_ind(y, True)), f(20_000_000 / 30 * dias_ind(y, True))]
             for t, y in [("6 meses", .5), ("1 año", 1), ("2 años", 2), ("5 años", 5), ("10 años", 10)]]
tab_ind = tabla(["Tiempo de servicio", "Días (menos de 10 SMMLV)", f"Indemnización con {f(SAL)}", "Días (≥ 10 SMMLV)", f"Indemnización con {f(20_000_000)}"], filas_ind, numericas=(1, 2, 3, 4))
i_indef = DIA * 60; i_fijo = DIA * 105

IND = f'''<p class="lead">La indemnización por despido sin justa causa es el pago que debe hacer el empleador cuando termina el contrato de forma unilateral y sin una razón que la ley reconozca. No es un regalo ni una bonificación: es una compensación obligatoria que regula el artículo 64 del Código Sustantivo del Trabajo (CST). Su valor depende de tres datos: el tipo de contrato, el salario y el tiempo de servicio.</p>
<h2>Cuándo hay derecho a indemnización</h2>
<p>Hay derecho a la indemnización cuando el empleador termina el contrato sin invocar una de las justas causas del artículo 62 del CST (por ejemplo, faltas graves del trabajador), o cuando invoca una causa que luego no logra demostrar. La carga de probar la justa causa es del empleador.</p>
<p>No hay indemnización en estos casos: renuncia voluntaria, terminación por mutuo acuerdo, vencimiento de un contrato a término fijo cuando el empleador avisó por escrito con al menos 30 días de antelación que no lo renovaría, o terminación por una justa causa debidamente probada.</p>
<div class="box"><p><b>Renuncia motivada (despido indirecto).</b> Si el trabajador renuncia porque el empleador incumplió gravemente sus obligaciones (por ejemplo, no pagarle el salario o aportar a seguridad social), la ley lo trata como un despido imputable al empleador y puede reclamar la indemnización. Se debe expresar la causa por escrito y puede requerir demostrarse ante un juez.</p></div>
<h2>Contrato a término indefinido</h2>
<p>La fórmula depende del salario:</p>
<ul>
<li><b>Salario menor a 10 SMMLV</b> (menos de {f(10*S)} en 2026): 30 días de salario por el primer año de servicio y 20 días por cada año adicional, proporcional por fracciones.</li>
<li><b>Salario de 10 SMMLV o más:</b> 20 días de salario por el primer año y 15 días por cada año adicional, proporcional por fracciones.</li>
</ul>
<p>Si el tiempo de servicio es de un año o menos, se pagan los 30 días (o 20 días) completos, sin proporcionalidad. La proporcionalidad solo aplica a las fracciones de año posteriores al primero. El valor de un día se obtiene dividiendo el salario mensual entre 30.</p>
{tab_ind}
<p><b>Ejemplo paso a paso.</b> Salario de {f(SAL)} y 900 días de servicio (2,5 años). Primer año: 30 días. Años siguientes: 1,5 años × 20 días = 30 días. Total: 60 días de salario. Como un día vale {f(SAL)} ÷ 30 = {f(DIA)}, la indemnización es 60 × {f(DIA)} = <b>{f(i_indef)}</b>.</p>
<h2>Contrato a término fijo</h2>
<p>En el contrato a término fijo la indemnización es el valor de los salarios del tiempo que falte para cumplir el plazo pactado. No importa cuánto tiempo lleve el trabajador: importa cuánto falta.</p>
<p><b>Ejemplo.</b> Contrato de 12 meses, del 1 de marzo de 2026 al 28 de febrero de 2027, con salario de {f(SAL)}. Si lo despiden sin justa causa el 15 de noviembre de 2026, faltan 105 días (15 de noviembre más diciembre, enero y febrero). Indemnización: 105 × {f(DIA)} = <b>{f(i_fijo)}</b>.</p>
<h2>Contrato por obra o labor</h2>
<p>Se pagan los salarios del tiempo que falte para terminar la obra o labor contratada, y la indemnización no puede ser inferior a 15 días de salario. Si faltaban 10 días para terminar la obra, se pagan igualmente 15 días: 15 × {f(DIA)} = {f(DIA*15)}.</p>
<h2>¿Sobre qué salario se calcula?</h2>
<p>Se usa el último salario devengado. Si el salario es variable (comisiones, horas extra frecuentes), se toma el promedio del último año o del tiempo de servicio si es menor (CST, art. 253). Los factores salariales, como las horas extra habituales y las comisiones, hacen parte de la base. Sobre si se incluye el auxilio de transporte hay criterios distintos; pide que tu liquidación indique expresamente la base usada.</p>
<h2>Qué más se paga al terminar el contrato</h2>
<p>La indemnización se suma a la liquidación ordinaria: cesantías, intereses sobre cesantías, prima proporcional, vacaciones pendientes y salario adeudado. Mira cómo se calcula cada uno en la <a href="como-se-calcula-la-liquidacion.html">guía de liquidación</a>.</p>
<h2>Si el empleador no paga a tiempo: indemnización moratoria</h2>
<p>Al terminar el contrato deben pagarse los salarios y prestaciones debidos. Si el empleador no lo hace, el artículo 65 del CST prevé la indemnización moratoria: un día de salario por cada día de retardo durante los primeros 24 meses y, después, intereses moratorios sobre las sumas adeudadas. La jurisprudencia exige que el juez analice la buena o mala fe del empleador, así que no es automática y normalmente se reclama en un proceso laboral.</p>
<h2>Situaciones con protección reforzada</h2>
<p>Algunos trabajadores tienen estabilidad laboral reforzada, por ejemplo mujeres en embarazo o lactancia, personas con discapacidad o con condiciones de salud que limitan su desempeño, y los aforados sindicales. En esos casos el despido puede requerir autorización previa del Ministerio del Trabajo, y si se hace sin ella puede ser ineficaz o generar indemnizaciones adicionales. Es un tema donde conviene asesoría profesional antes de actuar.</p>
<h2>Antes de firmar un acuerdo o un paz y salvo</h2>
<p>Pide por escrito el desglose de cada concepto, compáralo con las fórmulas de esta guía y no firmes si no entiendes un valor. Tienes 3 años para reclamar acreencias laborales desde que son exigibles (CST, art. 488). Puedes validar las cifras con un abogado laboral, un inspector del trabajo o el Ministerio del Trabajo.</p>'''

ARTICULOS.append(dict(
    file="indemnizacion.html", tag="Estabilidad laboral", calc="index.html#liq",
    h1="Indemnización por despido sin justa causa: cómo se calcula",
    title="Indemnización por despido sin justa causa en Colombia 2026 | Calculadora Laboral",
    desc="Cómo se calcula la indemnización por despido sin justa causa en contratos indefinidos, fijos y por obra o labor, con tablas, ejemplos y casos especiales.",
    card="Fórmulas por tipo de contrato, tabla por años de servicio, ejemplos y qué hacer si no te pagan.",
    resumen=["Indefinido con menos de 10 SMMLV: 30 días el primer año y 20 por cada año adicional.",
             "Contrato fijo: los salarios que faltan para terminar el plazo pactado.",
             "Obra o labor: los salarios que faltan, con un mínimo de 15 días.",
             "Si el empleador demora el pago, puede aplicar la indemnización moratoria del artículo 65."],
    body=IND,
    faq=[("¿Cuántos días de indemnización me corresponden si gano menos de 10 salarios mínimos?", "En contrato indefinido son 30 días de salario por el primer año de servicio y 20 días por cada año adicional, proporcional por fracciones."),
         ("¿El contrato a término fijo tiene mínimo de 15 días?", "No. En el contrato a término fijo se pagan los salarios del tiempo restante del plazo. El mínimo de 15 días aplica al contrato por obra o labor."),
         ("¿Hay indemnización si renuncio?", "No, salvo que la renuncia se base en un incumplimiento grave del empleador (despido indirecto), que debes sustentar por escrito."),
         ("¿Cuánto tiempo tengo para reclamar?", "Las acreencias laborales prescriben en 3 años desde que se hacen exigibles."),
         ("¿La indemnización incluye las cesantías y la prima?", "No. Se suma a la liquidación ordinaria, que incluye cesantías, intereses, prima proporcional y vacaciones pendientes.")],
    fuentes=[("Código Sustantivo del Trabajo, arts. 62, 64, 65 y 488 (art. 64 modificado por la Ley 789 de 2002)", None), F_CST, F_MT, F_GN]))

# ------------------------------------------------------------------ PILA
e1 = pila(5_000_000); e2 = pila(3_000_000); e3 = pila(20_000_000)
dias = [("00 a 07", 2), ("08 a 14", 3), ("15 a 21", 4), ("22 a 28", 5), ("29 a 35", 6), ("36 a 42", 7), ("43 a 49", 8), ("50 a 56", 9), ("57 a 63", 10), ("64 a 69", 11), ("70 a 75", 12), ("76 a 81", 13), ("82 a 87", 14), ("88 a 93", 15), ("94 a 99", 16)]
tabla_dias = tabla(["Últimos 2 dígitos", "Día hábil de pago"], [[a, str(b)] for a, b in dias], numericas=(1,))


def ex(r, titulo_ibc="IBC (40% de los ingresos, con piso de 1 SMMLV)"):
    filas = [[titulo_ibc, f(r["ibc"])], ["Salud 12,5%", f(r["salud"])], ["Pensión 16%", f(r["pension"])]]
    if r["fsp"]: filas.append([f"Fondo de Solidaridad Pensional {pc(r['fsp_r']*100)}%".replace(".", ","), f(r["fsp"])])
    filas += [["ARL riesgo I (0,522%)", f(r["arl"])], ["<b>Total a pagar</b>", f"<b>{f(r['total'])}</b>"]]
    return tabla(["Concepto", "Valor"], filas, numericas=(1,))


fsp_tab = tabla(["IBC (en SMMLV)", "Aporte al Fondo de Solidaridad"], [["Menos de 4", "0%"], ["De 4 a menos de 16", "1%"], ["De 16 a menos de 17", "1,2%"], ["De 17 a menos de 18", "1,4%"], ["De 18 a menos de 19", "1,6%"], ["De 19 a menos de 20", "1,8%"], ["20 o más", "2%"]], numericas=(1,))

PILA = f'''<p class="lead">Si trabajas por cuenta propia o con contrato de prestación de servicios, eres tú quien paga cada mes tu salud, tu pensión y tus riesgos laborales mediante la planilla PILA. Esta guía explica cómo se calcula cada aporte, cuándo se paga y qué errores evitar, con ejemplos con los valores de 2026: salario mínimo (SMMLV) de {f(S)}.</p>
<h2>Quién debe cotizar como independiente</h2>
<p>Deben cotizar los independientes y contratistas con ingresos mensuales iguales o superiores a 1 SMMLV. Si tus ingresos netos son menores y trabajas por días o semanas, desde septiembre de 2026 puedes cotizar pensión de forma proporcional con el <a href="pila-por-semanas-cotizante-76.html">tipo de cotizante 76</a>. También puedes consultar con tu EPS o un contador otras opciones, como el servicio social complementario BEPS para pensión.</p>
<h2>Paso 1: calcula tus ingresos netos del mes</h2>
<p>Parte de lo que facturaste o cobraste en el mes, sin IVA. Si tienes costos y gastos directamente relacionados con tu actividad y puedes soportarlos (arriendo de un local de trabajo, insumos, subcontratistas), se restan antes de seguir. La UGPP puede pedirte los soportes en una fiscalización, por eso conviene guardar facturas y cuentas de cobro por varios años.</p>
<h2>Paso 2: obtén tu IBC (el 40%)</h2>
<p>El ingreso base de cotización (IBC) es el 40% de tus ingresos netos mensuales. Tiene un piso de 1 SMMLV ({f(S)}) y un tope de 25 SMMLV ({f(25*S)}). Si el 40% queda por debajo del piso, se cotiza sobre el mínimo.</p>
<h2>Paso 3: aplica los porcentajes</h2>
<ul>
<li><b>Salud:</b> 12,5% del IBC.</li>
<li><b>Pensión:</b> 16% del IBC.</li>
<li><b>Fondo de Solidaridad Pensional:</b> 1% adicional cuando el IBC es de 4 SMMLV o más, con aumentos graduales hasta 2% (tabla abajo).</li>
<li><b>ARL:</b> según el riesgo de tu actividad. Riesgo I es 0,522% y llega a 6,96% en riesgo V. En riesgos IV y V la paga el contratante.</li>
<li><b>Caja de compensación:</b> opcional, 0,6% o 2% según el plan al que te afilies.</li>
</ul>
{fsp_tab}
<h2>Paso 4: redondea y suma</h2>
<p>La PILA redondea cada aporte hacia arriba al múltiplo de $100 más cercano. La suma de todos los aportes es el valor de tu planilla.</p>
<h2>Ejemplo 1: honorarios de {f(5_000_000)}</h2>
<p>El 40% de $ 5.000.000 es $ 2.000.000, que supera el piso. Con ARL de riesgo I y sin caja:</p>
{ex(e1)}
<h2>Ejemplo 2: honorarios de {f(3_000_000)} (aplica el piso)</h2>
<p>El 40% de $ 3.000.000 es $ 1.200.000, menor que 1 SMMLV. Se cotiza sobre {f(S)}:</p>
{ex(e2)}
<h2>Ejemplo 3: honorarios de {f(20_000_000)} (aplica el Fondo de Solidaridad)</h2>
<p>El 40% de $ 20.000.000 es $ 8.000.000, que equivale a más de 4 SMMLV ({f(4*S)}). Se suma el 1% del Fondo de Solidaridad Pensional:</p>
{ex(e3)}
<h2>¿Cuándo vence tu planilla?</h2>
<p>Pagas mes vencido: en noviembre pagas el período de octubre. El día límite depende de los dos últimos dígitos de tu cédula o NIT (Decreto 1990 de 2016) y se cuenta en días hábiles del mes siguiente:</p>
{tabla_dias}
<p class="meta">Contados de lunes a viernes sin festivos. Confirma la fecha exacta en tu operador PILA.</p>
<h2>Qué pasa si pagas tarde o no pagas</h2>
<p>Pagar después de la fecha límite genera intereses de mora que liquida el operador. Además, la UGPP fiscaliza a los independientes y puede sancionar omisiones o inexactitudes en la declaración de aportes. Dejar de cotizar también puede afectar la cobertura de tu EPS y la continuidad de tus semanas de pensión.</p>
<h2>Si eres contratista, revisa tu contrato</h2>
<p>El contratante debe afiliarte a la ARL, y en riesgos IV y V la paga él. Muchas entidades exigen la planilla pagada del mes anterior para pagarte los honorarios. Revisa que tu contrato diga qué costos pueden descontarse y guarda las cuentas de cobro: la herramienta de este sitio permite llevar ese seguimiento de cobros pendientes.</p>
<h2>Errores frecuentes</h2>
<ul>
<li>Cotizar sobre el 40% de lo recibido y olvidar que los costos solo se restan si están soportados.</li>
<li>Dejar de pagar un mes porque no hubo ingresos, sin informar la novedad correspondiente al operador.</li>
<li>Pagar la ARL de riesgo IV o V cuando le corresponde al contratante.</li>
<li>Cotizar un IBC distinto al de tus ingresos reales: la UGPP puede cruzar la información con la de la DIAN.</li>
<li>Olvidar el Fondo de Solidaridad Pensional cuando el IBC supera 4 SMMLV.</li>
</ul>'''

ARTICULOS.append(dict(
    file="guia-pila-2026.html", tag="Seguridad social", calc="index.html#pila",
    h1="Guía PILA 2026 para independientes: cómo calcular tu planilla paso a paso",
    title="Guía PILA 2026 para independientes: cómo calcular tu planilla | Calculadora Laboral",
    desc="Calcula tu PILA como independiente en 2026: IBC del 40%, salud, pensión, Fondo de Solidaridad, ARL, fechas de pago por cédula y tres ejemplos numéricos.",
    card="IBC del 40%, salud, pensión, solidaridad y ARL, con tres ejemplos y la tabla de fechas de pago.",
    resumen=["El IBC es el 40% de tus ingresos netos, con piso de 1 SMMLV y tope de 25.",
             "Pagas 12,5% a salud, 16% a pensión, ARL según riesgo y 1% o más al Fondo de Solidaridad desde 4 SMMLV de IBC.",
             "La fecha límite depende de los dos últimos dígitos de tu cédula o NIT."],
    body=PILA,
    faq=[("¿Cuánto debo pagar de seguridad social como independiente?", f"Sobre un IBC del 40% de tus ingresos netos pagas 12,5% de salud y 16% de pensión, más ARL. Con honorarios de {f(5_000_000)} el total de la planilla es {f(e1['total'])} con ARL riesgo I."),
         ("¿Qué pasa si mis ingresos son menores a un salario mínimo?", "La ley no te obliga a cotizar como independiente. Si trabajas por días o semanas, desde septiembre de 2026 puedes cotizar pensión de forma proporcional con el tipo de cotizante 76 (hay una guía en este sitio). También puedes consultar con tu EPS o un contador otras opciones de afiliación."),
         ("¿Cuándo debo pagar la PILA?", "Mes vencido, entre el día hábil 2 y el 16 del mes siguiente, según los dos últimos dígitos de tu cédula o NIT."),
         ("¿Puedo restar mis gastos antes de calcular el IBC?", "Sí, los costos y gastos directamente relacionados con tu actividad, siempre que puedas soportarlos ante la UGPP."),
         ("¿Quién paga la ARL si soy contratista?", "En riesgos I a III normalmente la paga el contratista y en riesgos IV y V la paga el contratante, que debe afiliarte.")],
    fuentes=[("Ley 100 de 1993 (Sistema de Seguridad Social Integral)", None), ("Ley 797 de 2003 (Fondo de Solidaridad Pensional)", None),
             ("Ley 1955 de 2019, art. 244 (IBC de independientes)", None), ("Decreto 723 de 2013 (afiliación de contratistas a la ARL)", None),
             ("Decreto 1990 de 2016 (plazos de pago de aportes)", None), F_UGPP, F_GN]))

# ------------------------------------------------------------------ PILA POR SEMANAS (COTIZANTE 76)
sem = []
for k, (rd, nm) in enumerate([("1 a 7", "1 semana"), ("8 a 14", "2 semanas"), ("15 a 21", "3 semanas"), ("22 a 30", "4 semanas")], 1):
    ibc_k = math.ceil(S * k / 4)
    sem.append([rd, nm, f"{k}/4", f(ibc_k), f(up(ibc_k * .16))])
tabla_sem = tabla(["Días trabajados en el mes", "Semanas", "Fracción del mínimo", "IBC de pensión", "Aporte a pensión (16%)"], sem, numericas=(3, 4))
arl76 = up(S * 0.00522)
ej_pen = up(math.ceil(S * 2 / 4) * .16)
ej_tot = ej_pen + arl76
ord_piso = pila(S)
ej76 = tabla(["Concepto", "Valor"], [["Pensión: 2 semanas, IBC de " + f(math.ceil(S * 2 / 4)) + " × 16%", f(ej_pen)],
                                      ["ARL riesgo I: 0,522% sobre 1 SMMLV (" + f(S) + ")", f(arl76)],
                                      ["Salud", "$ 0 (no se liquida en este tipo de cotizante)"],
                                      ["<b>Total de la planilla</b>", f"<b>{f(ej_tot)}</b>"]], numericas=(1,))

C76 = f'''<p class="lead">Si trabajas por días o por semanas y tus ingresos del mes no llegan a un salario mínimo, hasta hace poco tu opción de cotizar a pensión era pagar sobre un mínimo completo. Desde septiembre de 2026 la planilla PILA tiene el tipo de cotizante 76, "Trabajador de tiempo parcial independiente", que permite cotizar a pensión de forma proporcional a lo que trabajaste. Esta guía explica cómo funciona, cuánto se paga con el salario mínimo de 2026 ({f(S)}) y qué conviene confirmar antes de usarlo.</p>
<div class="box"><p><b>Qué está confirmado y qué conviene verificar</b></p><ul>
<li><b>Confirmado en el texto oficial:</b> la Resolución 1529 del 24 de julio de 2026 del Ministerio de Salud (Diario Oficial 53.566) crea el tipo "76. Trabajador de tiempo parcial Independiente", con base en el parágrafo 4 del artículo 34 de la Ley 2466 de 2025. En riesgos laborales se reportan 30 días con un salario mínimo de base, y la caja de compensación es voluntaria (0,6% o 2%).</li>
<li><b>Según la UGPP y la prensa especializada:</b> aplica para ingresos mensuales inferiores a 1 SMMLV, y los operadores deben habilitarlo para pagos desde el 1 de septiembre de 2026 (período de pensión de agosto). La fórmula del IBC por semanas está en el anexo técnico; los valores de la tabla siguen las cifras que han publicado esas fuentes y pueden diferir en pesos por redondeo.</li>
<li><b>Verifica siempre</b> con tu operador PILA que el tipo 76 esté habilitado para tu período y con tu EPS cómo queda tu salud.</li></ul></div>
<h2>Qué es el cotizante 76</h2>
<p>Es una forma de reportar tus aportes en la PILA cuando eres independiente, trabajas solo algunos días o semanas del mes y ganas menos de un salario mínimo. Antes de esta resolución, ese tipo de ingresos se reportaba con el tipo 51, pensado para trabajadores dependientes de tiempo parcial. La idea de la reforma laboral (Ley 2466 de 2025) es que puedas aportar a pensión en proporción a lo que realmente trabajas, sin pagar un mínimo completo cada mes.</p>
<p>La ley dice que los independientes "podrán" hacer cotizaciones proporcionales: es una opción, no una obligación general.</p>
<h2>Quién puede usarlo</h2>
<ul>
<li>Eres trabajador independiente de verdad, no un empleado con subordinación.</li>
<li>Trabajas por días o semanas, sin completar el mes.</li>
<li>Tus ingresos mensuales son inferiores a 1 SMMLV ({f(S)}).</li>
</ul>
<p>Según la UGPP, citada por la prensa, quedan por fuera los contratistas por prestación de servicios. Si firmas ese tipo de contrato, confirma tu caso con tu operador PILA o con la UGPP antes de elegir este tipo de cotizante. Si tus ingresos son de 1 SMMLV o más, sigues las reglas ordinarias de la <a href="guia-pila-2026.html">guía de PILA para independientes</a>.</p>
<h2>Cuánto se paga en pensión</h2>
<p>El IBC de pensión es una fracción del salario mínimo según las semanas que trabajaste en el mes, y el aporte es el 16% de ese IBC. Cada semana equivale a un cuarto del mínimo:</p>
{tabla_sem}
<p class="meta">Cálculo con el salario mínimo de 2026. La PILA redondea cada aporte hacia arriba al múltiplo de $100.</p>
<h2>Riesgos laborales (ARL)</h2>
<p>La ARL no es proporcional. Se reportan siempre 30 días y un IBC de 1 SMMLV, así que con riesgo I (0,522%) pagas {f(arl76)} al mes. La paga el trabajador.</p>
<h2>Salud y caja de compensación</h2>
<ul>
<li><b>Salud:</b> el texto oficial de este cotizante solo menciona pensión y riesgos laborales, y la prensa especializada indica que no se liquida aporte de salud. Eso no significa que quedes sin cobertura: debes tener tu afiliación por otra vía (por ejemplo, régimen subsidiado o como beneficiario de otra persona). Pregunta a tu EPS cuál es tu caso.</li>
<li><b>Caja de compensación:</b> es voluntaria, con tarifa de 0,6% o 2%.</li>
</ul>
<h2>Ejemplo: dos semanas de trabajo</h2>
<p>Trabajaste 12 días en el mes y recibiste unos $ 900.000, menos de un salario mínimo. Tus días caen en el rango de 8 a 14 días, es decir, dos semanas. Con ARL de riesgo I y sin caja de compensación:</p>
{ej76}
<p>Como referencia, si cotizaras como independiente ordinario sobre el mínimo (salud, pensión y ARL riesgo I), la planilla sería de {f(ord_piso["total"])}. La diferencia sale de pagar pensión solo por dos semanas y no liquidar salud.</p>
<h2>Cuándo conviene y cuándo no</h2>
<ul>
<li><b>Conviene</b> si trabajas pocos días, tus ingresos no llegan al mínimo y quieres seguir sumando semanas de pensión sin pagar un mes completo.</li>
<li><b>Mira bien</b> que el aporte es proporcional: al pagar menos, lo que acumulas para tu pensión también es menor. Pregunta a tu fondo de pensiones cómo se te cuentan esas semanas y compara con el servicio social complementario BEPS.</li>
<li><b>No aplica</b> si tus ingresos del mes alcanzan o superan 1 SMMLV.</li>
</ul>
<h2>Paso a paso para pagarlo</h2>
<ol>
<li>Cuenta los días que trabajaste en el mes y ubícalos en el rango de la tabla.</li>
<li>Confirma con tu operador PILA que el tipo de cotizante 76 está habilitado.</li>
<li>Reporta la novedad de ingreso y, cuando termines, la de retiro: en este tipo de cotizante son obligatorias.</li>
<li>Conserva los soportes de tus ingresos, los días trabajados y tu afiliación a salud, por si la UGPP te los pide.</li>
</ol>
<h2>Errores frecuentes</h2>
<ul>
<li>Usar el tipo 76 cuando tus ingresos del mes llegan o superan 1 SMMLV.</li>
<li>Elegirlo siendo contratista por prestación de servicios sin confirmarlo antes.</li>
<li>Reportar la ARL en proporción a los días: se reporta con 30 días y 1 SMMLV.</li>
<li>Olvidar las novedades de ingreso y retiro, que son obligatorias.</li>
<li>Asumir que queda cubierta tu salud sin revisar tu afiliación con la EPS.</li>
</ul>'''

ARTICULOS.append(dict(
    file="pila-por-semanas-cotizante-76.html", tag="Seguridad social", calc="index.html#pila",
    h1="PILA por días o semanas para independientes (cotizante 76): cuánto se paga en 2026",
    title="PILA por semanas: cotizante 76 para independientes 2026 | Calculadora Laboral",
    desc="Cómo cotizar pensión por días o semanas como independiente con ingresos menores a un salario mínimo: tipo 76, tabla de aportes 2026, ARL, salud y un ejemplo.",
    card="Tipo 76 de la PILA: cotiza pensión por semanas si ganas menos de un mínimo, con tabla de aportes 2026.",
    resumen=["Desde el 1 de septiembre de 2026 existe el tipo de cotizante 76 para independientes que trabajan por días o semanas y ganan menos de 1 SMMLV.",
             "La pensión se paga sobre 1/4, 2/4, 3/4 o 4/4 del mínimo según las semanas trabajadas; la ARL se paga siempre sobre 1 SMMLV.",
             "Confirma con tu operador PILA y tu EPS antes de usarlo, sobre todo si eres contratista por prestación de servicios."],
    body=C76,
    faq=[("¿Qué es el cotizante 76 en la PILA?", "Es el tipo \"Trabajador de tiempo parcial independiente\", creado por la Resolución 1529 de 2026 del Ministerio de Salud para quienes trabajan por días o semanas y ganan menos de un salario mínimo."),
         ("¿Cuánto pago de pensión si trabajé dos semanas?", f"Con el salario mínimo de 2026, el IBC es de {f(math.ceil(S * 2 / 4))} y el aporte del 16% es de {f(ej_pen)}, más la ARL, que se paga siempre sobre un salario mínimo."),
         ("¿Pago salud con el cotizante 76?", "El texto oficial solo menciona pensión y riesgos laborales, y no se liquida aporte de salud. Debes mantener tu afiliación por otra vía; consulta a tu EPS."),
         ("¿Lo puedo usar si soy contratista por prestación de servicios?", "Según la UGPP, citada por la prensa, los contratistas por prestación de servicios quedan excluidos. Confirma tu caso con tu operador PILA o con la UGPP."),
         ("¿Desde cuándo se puede pagar?", "Los operadores de PILA deben habilitarlo para pagos desde el 1 de septiembre de 2026, correspondientes al período de pensión de agosto.")],
    fuentes=[("Resolución 1529 de 2026 del Ministerio de Salud (texto en el normograma de la Cancillería)", "https://cancilleria.gov.co/normograma/compilacion/docs/resolucion_minsaludps_1529_2026.htm"),
             ("Ley 2466 de 2025 (reforma laboral), art. 34, parágrafo 4", None), ("Ley 100 de 1993 (Sistema de Seguridad Social Integral)", None), F_UGPP, F_GN]))

# ------------------------------------------------------------------ LIQUIDACIÓN
bc = SAL + AUX; ces = bc * 180 / 360; inte = ces * 180 * .12 / 360; pr = bc * 180 / 360; vac = SAL / 30 * 7.5; tot1 = ces + inte + pr + vac
s2 = 2_000_000; b2 = s2 + AUX
ces2 = b2 * 270 / 360; int2 = ces2 * 270 * .12 / 360; pri2 = b2 * 90 / 360; vac2 = s2 / 30 * (15 * 270 / 360); tot2 = ces2 + int2 + pri2 + vac2

LIQ = f'''<p class="lead">Cuando termina un contrato laboral, por renuncia, despido o vencimiento del plazo, el empleador debe liquidar todo lo que le adeuda al trabajador. Esta guía explica qué conceptos incluye, cómo se calcula cada uno y muestra dos ejemplos numéricos con los valores de 2026: SMMLV de {f(S)} y auxilio de transporte de {f(AUX)}.</p>
<h2>Qué incluye la liquidación</h2>
<ul>
<li><b>Cesantías:</b> un mes de salario por año de servicio (CST, art. 249). Ver la <a href="cesantias-e-intereses.html">guía de cesantías</a>.</li>
<li><b>Intereses sobre cesantías:</b> 12% anual sobre las cesantías causadas (Ley 52 de 1975).</li>
<li><b>Prima de servicios:</b> 30 días de salario por año, pagados por semestres (CST, art. 306). Ver la <a href="prima-de-servicios.html">guía de prima</a>.</li>
<li><b>Vacaciones pendientes:</b> 15 días hábiles por año trabajado (CST, art. 186). Ver la <a href="vacaciones.html">guía de vacaciones</a>.</li>
<li><b>Salario pendiente:</b> los días trabajados que aún no se han pagado.</li>
<li><b>Indemnización:</b> solo si el despido es sin justa causa (CST, art. 64). Ver la <a href="indemnizacion.html">guía de indemnización</a>.</li>
</ul>
<h2>Las bases de cálculo</h2>
<p>Los cálculos usan el año de 360 días (12 meses de 30 días). Cada concepto tiene su propia base:</p>
{tabla(["Concepto", "Base", "Incluye auxilio de transporte"], [["Cesantías", "Salario + auxilio de transporte", "Sí"], ["Intereses sobre cesantías", "Valor de las cesantías", "Sí, por derivación"], ["Prima de servicios", "Salario + auxilio de transporte", "Sí"], ["Vacaciones", "Salario ordinario", "No"]])}
<p>El auxilio de transporte se paga a quien devenga hasta 2 SMMLV ({f(2*S)} en 2026). Si tu salario es variable, la base es el promedio del último año o del tiempo trabajado si es menor.</p>
<h2>Las fórmulas</h2>
<ul>
<li>Cesantías = base × días trabajados ÷ 360.</li>
<li>Intereses = cesantías × días trabajados × 12% ÷ 360.</li>
<li>Prima = base × días del semestre trabajados ÷ 360.</li>
<li>Vacaciones = (salario ÷ 30) × (15 × días trabajados ÷ 360 − días ya disfrutados).</li>
</ul>
<h2>Ejemplo 1: contrato del 1 de enero al 30 de junio de 2026</h2>
<p>Salario de {f(SAL)} más auxilio de transporte: la base es {f(bc)}. Son 180 días de servicio.</p>
{tabla(["Concepto", "Valor"], [["Cesantías (180 días)", f(ces)], ["Intereses sobre cesantías", f(inte)], ["Prima de servicios (180 días)", f(pr)], ["Vacaciones (7,5 días hábiles)", f(vac)], ["<b>Total estimado</b>", f"<b>{f(tot1)}</b>"]], numericas=(1,))}
<h2>Ejemplo 2: contrato del 1 de enero al 30 de septiembre de 2026</h2>
<p>Salario de {f(s2)} más auxilio de transporte: la base es {f(b2)}. Son 270 días de servicio. La prima del primer semestre ya se pagó el 30 de junio, así que queda pendiente la del período de julio a septiembre (90 días).</p>
{tabla(["Concepto", "Cálculo", "Valor"], [["Cesantías (270 días)", f"{f(b2)} × 270 ÷ 360", f(ces2)], ["Intereses sobre cesantías", f"{f(ces2)} × 270 × 12% ÷ 360", f(int2)], ["Prima pendiente (90 días)", f"{f(b2)} × 90 ÷ 360", f(pri2)], ["Vacaciones (11,25 días hábiles)", f"{f(s2)} ÷ 30 × 11,25", f(vac2)], ["<b>Total estimado</b>", "", f"<b>{f(tot2)}</b>"]], numericas=(2,))}
<p>Si las cesantías ya se consignaron a un fondo, se descuentan de lo que se paga directamente. Si ya se pagaron las vacaciones en dinero o se disfrutaron, se restan los días correspondientes.</p>
<h2>Plazos y mora</h2>
<p>La liquidación debe pagarse al terminar el contrato. Si el empleador no lo hace, puede aplicar la indemnización moratoria del artículo 65 del CST (un día de salario por cada día de retardo en los primeros 24 meses). Antes de firmar un acuerdo de liquidación o un paz y salvo, valida las cifras con un abogado laboral o el Ministerio del Trabajo.</p>
<h2>Lo que este estimado no incluye</h2>
<p>No descuenta préstamos, libranzas ni retención en la fuente, y no considera todos los factores salariales variables (comisiones, horas extra) que modifican la base: si los tienes, usa el promedio que corresponda. Tampoco cubre la dotación ni conceptos pactados en tu contrato o convención colectiva. Los trabajadores con salario integral no reciben cesantías ni prima por separado.</p>
<h2>Checklist antes de firmar tu liquidación</h2>
<ol>
<li>Verifica las fechas de ingreso y retiro y los días totales.</li>
<li>Confirma que cada concepto tenga su base correcta (con o sin auxilio de transporte).</li>
<li>Revisa que se descuenten los pagos ya hechos de cesantías, prima y vacaciones.</li>
<li>Comprueba los aportes a seguridad social hasta la fecha de retiro.</li>
<li>Pide copia firmada de la carta de terminación y de la liquidación detallada.</li>
</ol>'''

ARTICULOS.append(dict(
    file="como-se-calcula-la-liquidacion.html", tag="Terminación del contrato", calc="index.html#liq",
    h1="Cómo se calcula la liquidación laboral en Colombia (2026)",
    title="Cómo se calcula la liquidación laboral en Colombia 2026 | Calculadora Laboral",
    desc="Cesantías, intereses, prima, vacaciones e indemnización: fórmulas, bases de cálculo y dos ejemplos completos de liquidación con los valores de 2026.",
    card="Cesantías, intereses, prima, vacaciones e indemnización con fórmulas, bases y dos ejemplos.",
    resumen=["La liquidación suma cesantías, intereses, prima, vacaciones y salario pendiente; la indemnización solo si el despido fue sin justa causa.",
             "Cesantías y prima usan salario más auxilio de transporte; las vacaciones usan solo el salario.",
             "Los cálculos usan el año de 360 días."],
    body=LIQ,
    faq=[("¿Cuánto tiempo tiene el empleador para pagar la liquidación?", "Debe pagarla al terminar el contrato. Si no lo hace, puede aplicar la indemnización moratoria del artículo 65 del CST."),
         ("¿El auxilio de transporte entra en las vacaciones?", "No. Las vacaciones se calculan con el salario ordinario, sin auxilio de transporte. Sí entra en las cesantías y la prima."),
         ("¿Si renuncio me pagan la liquidación completa?", "Sí: cesantías, intereses, prima proporcional y vacaciones pendientes. Lo único que no se paga es la indemnización por despido."),
         ("¿Cómo se calcula con salario variable?", "Se usa el promedio de lo devengado en el último año de servicio, o en el tiempo trabajado si es menor.")],
    fuentes=[("Código Sustantivo del Trabajo, arts. 65, 186, 249 y 306", None), ("Ley 52 de 1975 (intereses sobre cesantías)", None), F_CST, F_MT, F_GN]))

# ------------------------------------------------------------------ CESANTÍAS
def base_pr(sal):  # salario + auxilio si devenga hasta 2 SMMLV
    return sal + (AUX if sal <= 2 * S else 0)

filas_ces = [[f(s_), f(base_pr(s_)), f(base_pr(s_) * .12)] for s_ in (S, 2_500_000, SAL, 5_000_000)]
tab_ces = tabla(["Salario mensual", "Cesantías de un año completo", "Intereses (12%)"], [[a, b, c] for a, b, c in filas_ces], numericas=(1, 2))
c_ex = base_pr(SAL) * 200 / 360

CES = f'''<p class="lead">Las cesantías son una prestación social que funciona como un ahorro para quedarte sin ingresos o para financiar vivienda y estudio. Cada año el empleador debe reconocerte un mes de salario por cada año trabajado, además de los intereses sobre ese valor. Esta guía explica cómo se calculan, cuándo se pagan y qué sanciones existen si el empleador no cumple.</p>
<h2>Quién tiene derecho a las cesantías</h2>
<p>Tienen derecho los trabajadores dependientes con contrato laboral, sin importar si es a término fijo o indefinido. No las reciben los contratistas de prestación de servicios ni los trabajadores con salario integral, porque ese salario ya incluye el factor prestacional (CST, art. 132). El salario integral exige un mínimo de 13 SMMLV, es decir {f(13*S)} en 2026.</p>
<h2>Cómo se calculan</h2>
<p>La fórmula es: <b>cesantías = base × días trabajados ÷ 360</b>. La base es el último salario mensual más el auxilio de transporte si lo recibes. Si tu salario cambió durante el año o es variable, se usa el promedio de lo devengado en el último año (CST, art. 253).</p>
<p>Los intereses sobre cesantías son el 12% anual sobre las cesantías causadas: <b>intereses = cesantías × días ÷ 360 × 12%</b>.</p>
{tab_ces}
<p><b>Ejemplo con tiempo parcial.</b> Con salario de {f(SAL)} y auxilio, la base es {f(base_pr(SAL))}. Si trabajaste 200 días en el año: {f(base_pr(SAL))} × 200 ÷ 360 = <b>{f(c_ex)}</b> de cesantías. Los intereses serían {f(c_ex)} × 200 × 12% ÷ 360 = <b>{f(c_ex*200*.12/360)}</b>.</p>
<h2>Fechas límite que debes conocer</h2>
{tabla(["Fecha", "Obligación del empleador"], [["31 de enero", "Pagar directamente al trabajador los intereses sobre cesantías del año anterior."], ["14 de febrero", "Consignar las cesantías del año anterior en el fondo elegido por el trabajador."]])}
<h2>Sanciones por incumplimiento</h2>
<ul>
<li><b>No consignar las cesantías a más tardar el 14 de febrero:</b> el empleador debe pagar un día de salario por cada día de retardo (Ley 50 de 1990, art. 99).</li>
<li><b>No pagar los intereses a tiempo:</b> debe pagar, además de los intereses, una suma adicional equivalente al valor de los intereses adeudados (Ley 52 de 1975).</li>
</ul>
<p>Si tu empleador no consignó, pide a tu fondo el extracto del año y compáralo con tus cálculos. Si hay diferencia, solicita por escrito la corrección.</p>
<h2>Régimen de consignación y régimen retroactivo</h2>
<p>La mayoría de los trabajadores está en el régimen de la Ley 50 de 1990, en el que las cesantías se consignan cada año en un fondo (Porvenir, Protección, Colfondos, Skandia o el Fondo Nacional del Ahorro, entre otros). Algunos contratos anteriores a 1991 siguen en el régimen retroactivo, donde las cesantías se calculan sobre el último salario por todo el tiempo de servicio y se pagan al retiro. Si tu contrato es reciente, estás en el primero.</p>
<h2>Cuándo puedes retirar las cesantías</h2>
<ul>
<li>Al terminar el contrato: el empleador firma la carta de retiro y el fondo entrega el dinero.</li>
<li>Retiros parciales: para comprar, construir, mejorar o liberar de gravámenes una vivienda, y para estudios propios, del cónyuge o de los hijos (CST, art. 256).</li>
</ul>
<p>Retirar en un momento sin necesidad de gasto reduce tu ahorro para un eventual desempleo, así que conviene hacerlo solo cuando lo necesites.</p>
<h2>Cesantías en el contrato por pocos meses</h2>
<p>También se pagan de forma proporcional. Una persona que trabajó 90 días con salario de {f(SAL)} y auxilio recibe {f(base_pr(SAL))} × 90 ÷ 360 = {f(base_pr(SAL)*90/360)} en cesantías. Se incluyen en la <a href="como-se-calcula-la-liquidacion.html">liquidación final</a> junto con los demás conceptos.</p>'''

ARTICULOS.append(dict(
    file="cesantias-e-intereses.html", tag="Prestaciones sociales", calc="index.html#liq",
    h1="Cesantías e intereses sobre cesantías: cómo se calculan en 2026",
    title="Cesantías e intereses sobre cesantías 2026: cálculo y fechas | Calculadora Laboral",
    desc="Cómo calcular las cesantías y sus intereses del 12% en Colombia, con tabla por salario, fechas límite (31 de enero y 14 de febrero), sanciones y retiros.",
    card="Fórmula, tabla por salario, fechas del 31 de enero y 14 de febrero, sanciones y retiros parciales.",
    resumen=["Cesantías = (salario + auxilio de transporte) × días ÷ 360. Los intereses son el 12% anual sobre ese valor.",
             "El empleador paga los intereses a más tardar el 31 de enero y consigna las cesantías antes del 15 de febrero.",
             "Si no consigna a tiempo, debe un día de salario por cada día de retraso."],
    body=CES,
    faq=[("¿Los contratistas tienen cesantías?", "No. Solo los trabajadores dependientes con contrato laboral y salario ordinario las reciben."),
         ("¿Cuándo me pagan los intereses de las cesantías?", "A más tardar el 31 de enero del año siguiente, directamente al trabajador."),
         ("¿Qué pasa si mi empleador no consigna las cesantías?", "Debe pagar un día de salario por cada día de retardo después del 14 de febrero (Ley 50 de 1990, art. 99)."),
         ("¿Se calculan con auxilio de transporte?", "Sí. La base de las cesantías es el salario más el auxilio de transporte, si lo recibes."),
         ("¿Puedo retirarlas sin haber terminado el contrato?", "Solo para vivienda y estudio, en los términos del artículo 256 del CST.")],
    fuentes=[("Código Sustantivo del Trabajo, arts. 132, 249, 253 y 256", None), ("Ley 50 de 1990, art. 99 (régimen de consignación y sanción)", None), ("Ley 52 de 1975 (intereses sobre cesantías)", None), F_CST, F_MT, F_GN]))

# ------------------------------------------------------------------ PRIMA
tab_prima = tabla(["Salario mensual", "Base (con auxilio si aplica)", "Prima de un semestre completo"],
                  [[f(s_), f(base_pr(s_)), f(base_pr(s_) / 2)] for s_ in (S, 2_500_000, SAL, 5_000_000)], numericas=(1, 2))
PRIMA = f'''<p class="lead">La prima de servicios es el pago de 30 días de salario por cada año trabajado, dividido en dos cuotas semestrales. Es una de las prestaciones que más se espera en junio y diciembre, y también una de las que más se liquidan mal cuando el salario cambia o se trabajó solo parte del semestre.</p>
<h2>Cuánto es y cuándo se paga</h2>
<p>Por cada semestre completo trabajado corresponden 15 días de salario. Se paga en dos fechas:</p>
{tabla(["Semestre trabajado", "Fecha máxima de pago"], [["1 de enero a 30 de junio", "30 de junio"], ["1 de julio a 31 de diciembre", "20 de diciembre"]])}
<h2>La fórmula</h2>
<p><b>Prima = base × días trabajados en el semestre ÷ 360.</b> La base es el salario mensual más el auxilio de transporte si lo recibes. Para un semestre completo (180 días), esto equivale a la mitad de la base.</p>
{tab_prima}
<p>Si tu salario supera 2 SMMLV ({f(2*S)}) no hay auxilio de transporte, y la prima se calcula solo sobre el salario.</p>
<h2>Salario variable o con cambios en el semestre</h2>
<p>Si tu salario es fijo durante el semestre, la base es el último salario devengado. Si tuviste aumentos durante el período o ingresos variables, como comisiones, horas extra o recargos, la base es el promedio de lo devengado en el semestre (CST, art. 308).</p>
<h2>Si trabajaste menos de un semestre</h2>
<p>Se paga proporcional a los días laborados. <b>Ejemplo:</b> una persona ingresó el 1 de abril con salario de {f(SAL)} y auxilio. Trabajó 90 días del primer semestre. Prima = {f(base_pr(SAL))} × 90 ÷ 360 = <b>{f(base_pr(SAL)*90/360)}</b>. Si el contrato termina antes del 30 de junio, esa prima se paga dentro de la liquidación.</p>
<h2>Qué días no cuentan</h2>
<p>Los días de suspensión del contrato, como licencias no remuneradas o suspensiones disciplinarias, se descuentan de los días trabajados. En cambio, las vacaciones y las incapacidades pagadas por el empleador o la EPS no restan días para efectos de la prima.</p>
<h2>¿Y los contratistas?</h2>
<p>La prima no se paga en contratos de prestación de servicios, porque no hay relación laboral. Si trabajas como independiente, no recibes prima, pero sí debes pagar tus aportes por tu cuenta. Revisa la <a href="guia-pila-2026.html">guía de PILA</a> y la comparación entre <a href="contratista-vs-empleado.html">contratista y empleado</a>.</p>
<h2>Qué hacer si no te pagan la prima</h2>
<p>Pregunta primero por escrito si el pago tiene fecha distinta o si hubo un error de cálculo. Guarda tu desprendible y contrato. Si hay incumplimiento, puedes acudir a la inspección del Ministerio del Trabajo. La prima prescribe a los 3 años desde que es exigible.</p>'''

ARTICULOS.append(dict(
    file="prima-de-servicios.html", tag="Prestaciones sociales", calc="index.html#liq",
    h1="Prima de servicios 2026: cómo se calcula y cuándo se paga",
    title="Prima de servicios 2026 en Colombia: cálculo y fechas de pago | Calculadora Laboral",
    desc="Cómo calcular la prima de servicios (30 de junio y 20 de diciembre): fórmula, base con auxilio de transporte, tabla por salario y casos de tiempo parcial.",
    card="Fórmula, fechas del 30 de junio y 20 de diciembre, tabla por salario y casos de tiempo parcial.",
    resumen=["La prima equivale a 30 días de salario por año, pagados en dos cuotas: 30 de junio y 20 de diciembre.",
             "Se calcula como base × días del semestre ÷ 360, con salario más auxilio de transporte.",
             "Si trabajaste menos de un semestre, se paga proporcional."],
    body=PRIMA,
    faq=[("¿Cuándo se paga la prima de servicios?", "La del primer semestre a más tardar el 30 de junio y la del segundo a más tardar el 20 de diciembre."),
         ("¿La prima incluye el auxilio de transporte?", "Sí, si ganas hasta 2 SMMLV el auxilio hace parte de la base."),
         ("¿Cuánto me corresponde si entré en la mitad del semestre?", "Se paga proporcional: base × días trabajados ÷ 360."),
         ("¿Los contratistas reciben prima?", "No, porque no tienen relación laboral.")],
    fuentes=[("Código Sustantivo del Trabajo, arts. 306 a 308", None), F_CST, F_MT, F_GN]))

# ------------------------------------------------------------------ VACACIONES
tab_vac = tabla(["Salario mensual", "15 días hábiles (año completo)", "7,5 días (la mitad en dinero)"],
                [[f(s_), f(s_ / 30 * 15), f(s_ / 30 * 7.5)] for s_ in (S, 2_500_000, SAL, 5_000_000)], numericas=(1, 2))
VAC = f'''<p class="lead">Las vacaciones son 15 días hábiles de descanso remunerado por cada año de servicio. Parece simple, pero hay detalles que generan confusión: qué días cuentan, cuánto se paga, cuánto se puede cambiar por dinero y qué pasa cuando termina el contrato. Aquí está todo con ejemplos de 2026.</p>
<h2>Cuántos días te corresponden</h2>
<p>Por cada año de servicio tienes derecho a 15 días hábiles consecutivos de vacaciones remuneradas (CST, art. 186). Los días hábiles son los días en que normalmente trabaja la empresa: si tu empresa trabaja de lunes a sábado, el sábado cuenta como día hábil; los domingos y festivos no cuentan.</p>
<p>El derecho se causa al cumplir el año, pero se va acumulando proporcionalmente: por cada 360 días trabajados corresponden 15 días, es decir, 1,25 días por mes.</p>
<h2>Cuánto se paga</h2>
<p>Las vacaciones se pagan con el salario ordinario vigente al momento en que empiezas a disfrutarlas (CST, art. 192). El auxilio de transporte no hace parte de esta base. Si tu salario es variable, se promedia lo devengado en el último año. La forma sencilla de calcularlo es: <b>valor = salario ÷ 30 × días</b>.</p>
{tab_vac}
<h2>Compensación en dinero</h2>
<p>La ley permite compensar en dinero hasta la mitad de las vacaciones si hay acuerdo entre el trabajador y el empleador (CST, art. 189). Es decir, se disfrutan al menos 7,5 días y los restantes se pagan sin descansar. Ten presente:</p>
<ul>
<li>El descanso de seis días hábiles continuos al año no es compensable (CST, art. 190).</li>
<li>Los días disfrutados se pagan como tu salario normal. Los compensados se pagan aparte, además del salario por los días que trabajaste.</li>
<li>Con un salario de {f(SAL)}, compensar 7,5 días equivale a {f(SAL/30*7.5)}.</li>
</ul>
<h2>Cuándo se toman</h2>
<p>El empleador señala la época sin afectar la efectividad del descanso, y debe avisarte con 15 días de anticipación la fecha en que las concederá (CST, art. 187). Lo ideal es acordar la fecha por escrito y dejar constancia del período disfrutado.</p>
<h2>Vacaciones proporcionales al terminar el contrato</h2>
<p>Si el contrato termina sin que hayas cumplido el año o con días pendientes, se pagan en dinero de forma proporcional. <b>Ejemplo:</b> salario de {f(SAL)} y 180 días trabajados. Días causados: 15 × 180 ÷ 360 = 7,5. Valor: {f(SAL)} ÷ 30 × 7,5 = <b>{f(SAL/30*7.5)}</b>. Con 270 días serían 11,25 días y {f(SAL/30*11.25)}.</p>
<p>Si ya disfrutaste parte de las vacaciones, se descuentan esos días del total causado. Mira el detalle en la <a href="como-se-calcula-la-liquidacion.html">guía de liquidación</a>.</p>
<h2>Si no te han dado vacaciones</h2>
<p>Pregunta por escrito cuántos días tienes causados y propón fechas. La acumulación de vacaciones sin disfrutar solo se permite en casos excepcionales, como por ejemplo para trabajadores técnicos, especializados o de confianza, hasta por dos años. Si te las niegan sistemáticamente, puedes acudir al Ministerio del Trabajo.</p>
<h2>Vacaciones y contratistas</h2>
<p>Los contratistas de prestación de servicios no tienen vacaciones remuneradas por ley. Es una de las diferencias más relevantes frente a un contrato laboral, que se explica en la guía de <a href="contratista-vs-empleado.html">contratista y empleado</a>.</p>'''

ARTICULOS.append(dict(
    file="vacaciones.html", tag="Prestaciones sociales", calc="index.html#vac",
    h1="Vacaciones en Colombia: cómo se calculan, cuánto se paga y cuándo compensarlas",
    title="Vacaciones en Colombia 2026: cálculo, pago y compensación | Calculadora Laboral",
    desc="Cómo calcular tus vacaciones: 15 días hábiles por año, base de pago, compensación en dinero, proporcionales al terminar el contrato y ejemplos con valores de 2026.",
    card="15 días hábiles, base de pago, compensación en dinero y proporcionales con ejemplos numéricos.",
    resumen=["Tienes derecho a 15 días hábiles remunerados por cada año de servicio.",
             "Se pagan con el salario ordinario, sin auxilio de transporte: salario ÷ 30 × días.",
             "Se puede compensar en dinero hasta la mitad con acuerdo entre las partes."],
    body=VAC,
    faq=[("¿Cuántos días de vacaciones me corresponden?", "15 días hábiles por cada año de servicio, que se causan proporcionalmente (1,25 días por mes)."),
         ("¿Las vacaciones se calculan con auxilio de transporte?", "No. Se calculan con el salario ordinario, sin auxilio de transporte."),
         ("¿Puedo cambiar todas mis vacaciones por dinero?", "No. Solo se puede compensar hasta la mitad y con acuerdo entre las partes."),
         ("¿Cuánto me pagan de vacaciones si me voy de la empresa?", "Se pagan en dinero las vacaciones causadas y no disfrutadas, de forma proporcional al tiempo trabajado.")],
    fuentes=[("Código Sustantivo del Trabajo, arts. 186 a 192", None), F_CST, F_MT, F_GN]))

# ------------------------------------------------------------------ SALARIO MÍNIMO
um = [("1 SMMLV", 1, "Piso de cotización de independientes y empleados; referencia del salario mínimo."), ("2 SMMLV", 2, "Quien gana hasta este valor recibe auxilio de transporte y dotación."),
      ("4 SMMLV", 4, "Desde este IBC se aporta al Fondo de Solidaridad Pensional."), ("10 SMMLV", 10, "Cambia la fórmula de indemnización por despido; límite de la exoneración de aportes del empleador."),
      ("13 SMMLV", 13, "Mínimo para pactar salario integral."), ("25 SMMLV", 25, "Tope del IBC para cotizar a seguridad social.")]
tab_um = tabla(["Umbral", "Valor en 2026", "Para qué sirve"], [[a, f(S * m), c] for a, m, c in um], numericas=(1,))
SMM = f'''<p class="lead">El salario mínimo es la base de casi todos los cálculos laborales: aportes, indemnizaciones, auxilio de transporte, límites de cotización. Para 2026 el salario mínimo mensual legal vigente (SMMLV) es de <b>{f(S)}</b> y el auxilio de transporte de <b>{f(AUX)}</b>. Esta guía reúne los valores y los umbrales que se derivan de ellos.</p>
<h2>Valores vigentes en 2026</h2>
{tabla(["Concepto", "Valor"], [["Salario mínimo mensual (SMMLV)", f(S)], ["Auxilio de transporte mensual", f(AUX)], ["SMMLV más auxilio de transporte", f(S + AUX)], ["Salario mínimo diario (÷ 30)", f(S / 30)], ["Valor de la hora ordinaria (÷ 210, jornada de 42 horas)", f(S / 210)]], numericas=(1,))}
<p>Estos valores corresponden a los Decretos 1469 y 1470 de 2025. El decreto del salario mínimo fue objeto de una medida cautelar del Consejo de Estado en 2026 que posteriormente se levantó. Los valores de esta página son los vigentes en la fecha de actualización; verifica siempre la normativa más reciente.</p>
<h2>Los umbrales que debes conocer</h2>
<p>Muchas reglas laborales se activan por múltiplos del salario mínimo:</p>
{tab_um}
<h2>Auxilio de transporte: quién lo recibe</h2>
<ul>
<li>Lo reciben los trabajadores que devengan hasta 2 SMMLV ({f(2*S)} en 2026) y que deben desplazarse para ir al trabajo.</li>
<li>Se paga por los días efectivamente trabajados. No se suele pagar durante vacaciones, licencias o incapacidades.</li>
<li>No hace parte de la base de aportes a seguridad social, pero sí de las cesantías y de la prima.</li>
<li>Para el trabajo en casa y el teletrabajo, el auxilio de conectividad digital reemplaza al de transporte (Ley 2121 de 2021).</li>
<li>Los contratistas de prestación de servicios no lo reciben.</li>
</ul>
<h2>Dotación</h2>
<p>Los trabajadores que ganan hasta 2 SMMLV y llevan más de tres meses de servicio tienen derecho a tres entregas de calzado y vestido de labor al año, normalmente el 30 de abril, el 31 de agosto y el 20 de diciembre (CST, art. 230).</p>
<h2>Ejemplo: de qué se compone un salario mínimo</h2>
<p>Una persona que gana el salario mínimo con auxilio de transporte tiene una base de {f(S+AUX)} para cesantías y prima. Cada mes aporta el 4% de {f(S)} a salud ({f(S*.04)}) y el 4% a pensión ({f(S*.04)}). Su pago neto del mes es {f(S - 2*S*.04 + AUX)}. Para ver el costo completo para la empresa, mira la guía de <a href="costo-real-de-un-empleado.html">costo real de un empleado</a>.</p>'''

ARTICULOS.append(dict(
    file="salario-minimo-auxilio-transporte-2026.html", tag="Cifras 2026", calc="index.html#sueldo",
    h1="Salario mínimo y auxilio de transporte 2026: valores y umbrales clave",
    title="Salario mínimo y auxilio de transporte 2026 en Colombia | Calculadora Laboral",
    desc="Valores del salario mínimo ($1.750.905) y del auxilio de transporte ($249.095) en 2026, quién los recibe y qué umbrales activan cada regla laboral.",
    card="Valores 2026, quién recibe auxilio y los umbrales de 2, 4, 10, 13 y 25 SMMLV.",
    resumen=[f"SMMLV 2026: {f(S)}. Auxilio de transporte: {f(AUX)}.",
             "Hasta 2 SMMLV se recibe auxilio de transporte y dotación.",
             "Los umbrales de 4, 10, 13 y 25 SMMLV cambian la cotización, la indemnización y el salario integral."],
    body=SMM,
    faq=[("¿Cuál es el salario mínimo en Colombia en 2026?", f"{f(S)} mensuales, más {f(AUX)} de auxilio de transporte para quienes ganan hasta 2 salarios mínimos."),
         ("¿Quién recibe el auxilio de transporte?", f"Los trabajadores que devengan hasta 2 SMMLV ({f(2*S)}), por los días efectivamente trabajados."),
         ("¿Cuál es el valor de la hora ordinaria con salario mínimo?", f"Con jornada de 42 horas, {f(S)} ÷ 210 = {f(S/210)}."),
         ("¿Cuál es el salario mínimo para el salario integral?", f"13 SMMLV, es decir {f(13*S)} en 2026.")],
    fuentes=[("Decreto 1469 de 2025 (salario mínimo 2026)", None), ("Decreto 1470 de 2025 (auxilio de transporte 2026)", None), ("Ley 2121 de 2021 (auxilio de conectividad digital)", None), F_CST, F_MT, F_GN]))

# ------------------------------------------------------------------ COSTO REAL DE UN EMPLEADO
bcx = SAL + AUX
e_pen = SAL * .12; e_sal = SAL * .085; e_arl = SAL * .00522; e_caja = SAL * .04; e_sena = SAL * .02; e_icbf = SAL * .03
p_ces = bcx / 12; p_int = p_ces * .12; p_pri = bcx / 12; p_vac = SAL * 15 / 360
ss_exo = e_pen + e_arl + e_caja
ss_full = ss_exo + e_sal + e_sena + e_icbf
prest = p_ces + p_int + p_pri + p_vac
cost_exo = bcx + ss_exo + prest
cost_full = bcx + ss_full + prest
neto = SAL - SAL * .04 - SAL * .04 + AUX

COSTO = f'''<p class="lead">Contratar a una persona con un salario de {f(SAL)} no cuesta {f(SAL)} al mes. Entre aportes a seguridad social, parafiscales y prestaciones, el costo real para la empresa es sensiblemente mayor. Esta guía desglosa cada componente con el mismo ejemplo, tanto para quien contrata como para quien quiere entender qué hay detrás de su sueldo.</p>
<h2>Los tres bloques del costo</h2>
<ol>
<li><b>Salario y auxilio de transporte:</b> lo que se paga directamente a la persona.</li>
<li><b>Aportes del empleador:</b> seguridad social y parafiscales, que se calculan sobre el salario sin el auxilio de transporte.</li>
<li><b>Prestaciones sociales y vacaciones:</b> cesantías, intereses, prima y vacaciones, que se provisionan mes a mes.</li>
</ol>
<h2>Aportes del empleador</h2>
{tabla(["Aporte", "Porcentaje", f"Valor sobre {f(SAL)}"], [
 ["Pensión", "12%", f(e_pen)], ["Salud", "8,5%", f(e_sal)], ["ARL riesgo I", "0,522%", f(e_arl)],
 ["Caja de compensación", "4%", f(e_caja)], ["SENA", "2%", f(e_sena)], ["ICBF", "3%", f(e_icbf)]], numericas=(1, 2))}
<p>Hay una exoneración importante: las personas jurídicas (y las personas naturales con dos o más trabajadores) que contratan empleados que ganan menos de 10 SMMLV ({f(10*S)}) están exoneradas de pagar salud (8,5%), SENA (2%) e ICBF (3%) (Estatuto Tributario, art. 114-1). Siempre deben pagar pensión, ARL y caja de compensación.</p>
<h2>Prestaciones que se provisionan cada mes</h2>
<p>La base de cesantías y prima es salario más auxilio ({f(bcx)}). Mes a mes, la empresa debe reservar:</p>
{tabla(["Prestación", "Cálculo mensual", "Valor"], [
 ["Cesantías", "base ÷ 12", f(p_ces)], ["Intereses sobre cesantías", "cesantías × 12% (anual, prorrateado)", f(p_int)],
 ["Prima de servicios", "base ÷ 12", f(p_pri)], ["Vacaciones", "salario × 15 ÷ 360", f(p_vac)],
 ["<b>Total prestaciones</b>", "", f"<b>{f(prest)}</b>"]], numericas=(2,))}
<h2>Costo mensual total para la empresa</h2>
{tabla(["Componente", "Con exoneración", "Sin exoneración"], [
 ["Salario", f(SAL), f(SAL)], ["Auxilio de transporte", f(AUX), f(AUX)],
 ["Aportes del empleador", f(ss_exo), f(ss_full)], ["Prestaciones y vacaciones", f(prest), f(prest)],
 ["<b>Costo mensual</b>", f"<b>{f(cost_exo)}</b>", f"<b>{f(cost_full)}</b>"],
 ["Sobre el salario", f"+{pc(round((cost_exo/SAL-1)*100, 1))}%", f"+{pc(round((cost_full/SAL-1)*100, 1))}%"]], numericas=(1, 2))}
<p>Es decir, una persona que recibe {f(SAL)} de salario le cuesta a la empresa entre {f(cost_exo)} y {f(cost_full)} al mes, sin contar dotación, capacitación ni otros beneficios pactados. Para el empleador la regla práctica es que el costo ronda entre {f"{cost_exo/SAL:.2f}".replace(".", ",")} y {f"{cost_full/SAL:.2f}".replace(".", ",")} veces el salario según la exoneración.</p>
<h2>Lo que recibe el empleado: del salario al neto</h2>
<p>Del salario, el trabajador aporta el 4% a salud y el 4% a pensión. Con {f(SAL)}: {f(SAL*.04)} + {f(SAL*.04)} = {f(SAL*.08)}. Con el auxilio de transporte, el pago neto del mes es {f(SAL)} − {f(SAL*.08)} + {f(AUX)} = <b>{f(neto)}</b>. Si el salario es de 4 SMMLV o más ({f(4*S)}), se suma además el aporte al Fondo de Solidaridad Pensional.</p>
<h2>Para quién es útil este cálculo</h2>
<ul>
<li><b>Quien va a contratar por primera vez:</b> para presupuestar sin sorpresas y entender cuánto se provisiona cada mes.</li>
<li><b>Quien recibe un salario:</b> para verificar que los aportes y el neto de su desprendible son coherentes.</li>
<li><b>Quien compara una oferta laboral con un contrato de prestación de servicios:</b> el contratista asume sus propios aportes y no recibe prestaciones. Ver la guía de <a href="contratista-vs-empleado.html">contratista y empleado</a>.</li>
</ul>'''

ARTICULOS.append(dict(
    file="costo-real-de-un-empleado.html", tag="Para empleadores y empleados", calc="index.html#sueldo",
    h1="Costo real de un empleado en Colombia: aportes, prestaciones y neto (2026)",
    title="Costo real de un empleado en Colombia 2026: aportes y prestaciones | Calculadora Laboral",
    desc="Cuánto cuesta realmente un empleado: aportes del empleador, exoneración del artículo 114-1, prestaciones sociales y el neto que recibe el trabajador, con un ejemplo completo.",
    card="Aportes del empleador, exoneración, prestaciones y neto del trabajador con un ejemplo completo.",
    resumen=[f"Con un salario de {f(SAL)}, el costo mensual para la empresa va de {f(cost_exo)} a {f(cost_full)}.",
             "La exoneración del art. 114-1 del ET elimina salud, SENA e ICBF para salarios menores a 10 SMMLV.",
             f"El empleado aporta 4% a salud y 4% a pensión: con auxilio, su neto es {f(neto)}."],
    body=COSTO,
    faq=[("¿Cuánto aporta el empleador a seguridad social?", "Pensión 12%, salud 8,5%, ARL según el riesgo, caja de compensación 4%, SENA 2% e ICBF 3%. Salud, SENA e ICBF pueden estar exonerados."),
         ("¿Qué aporta el empleado?", "El 4% de su salario a salud y el 4% a pensión, descontados por nómina."),
         ("¿Los aportes se calculan sobre el auxilio de transporte?", "No. Se calculan sobre el salario. El auxilio de transporte sí hace parte de la base de cesantías y prima."),
         ("¿Quién puede acceder a la exoneración?", "Personas jurídicas y personas naturales con dos o más trabajadores, respecto de los empleados que ganan menos de 10 SMMLV.")],
    fuentes=[("Ley 100 de 1993 (aportes a salud y pensión)", None), ("Estatuto Tributario, art. 114-1 (exoneración de aportes)", None), ("Código Sustantivo del Trabajo, arts. 249, 306 y 186", None), F_UGPP, F_GN]))

# ------------------------------------------------------------------ CONTRATISTA VS EMPLEADO
CVE = f'''<p class="lead">Muchas personas trabajan con "contrato de prestación de servicios" cuando en realidad cumplen horarios y reciben órdenes como cualquier empleado. Y muchas empresas contratan de buena fe a un contratista que de verdad es independiente. Entender la diferencia protege a las dos partes. Esta guía explica los criterios, las consecuencias y qué hacer si tienes dudas.</p>
<h2>Las diferencias de fondo</h2>
{tabla(["Aspecto", "Contrato de trabajo", "Prestación de servicios"], [
 ["Naturaleza", "Relación laboral con subordinación", "Contrato civil o comercial con autonomía"],
 ["Pago", "Salario", "Honorarios por servicios o entregables"],
 ["Horario", "Lo fija el empleador", "Lo organiza el contratista"],
 ["Herramientas", "Normalmente las pone la empresa", "Normalmente las pone el contratista"],
 ["Cesantías, prima, vacaciones", "Sí", "No"],
 ["Seguridad social", "Aporta el empleador (y el empleado)", "Lo paga el contratista sobre el 40% de sus ingresos"],
 ["Indemnización por despido", "Sí, si es sin justa causa", "Solo si el contrato lo pacta"],
 ["Auxilio de transporte y dotación", "Sí, hasta 2 SMMLV", "No"]])}
<h2>Los tres elementos del contrato de trabajo</h2>
<p>El artículo 23 del CST define el contrato de trabajo por tres elementos: la actividad personal del trabajador, la continuada subordinación o dependencia, y un salario como retribución. Cuando se demuestra que una persona prestó un servicio personal, la ley presume que existe contrato de trabajo (CST, art. 24), y le corresponde a quien lo niega probar lo contrario.</p>
<h2>Contrato realidad</h2>
<p>En derecho laboral colombiano prima la realidad sobre las formas (Constitución Política, art. 53). El nombre que le pongan al contrato no es lo decisivo: si en los hechos hay subordinación, un juez puede declarar la existencia de un contrato de trabajo y ordenar el pago de prestaciones, aportes e indemnizaciones.</p>
<h2>Señales de subordinación</h2>
<ul>
<li>Cumplir un horario impuesto y rendir cuentas de ausencias.</li>
<li>Recibir órdenes sobre cómo hacer el trabajo, no solo qué entregar.</li>
<li>Trabajar con herramientas, correo o instalaciones de la empresa, con jefe directo.</li>
<li>Exclusividad: no poder trabajar para otros clientes.</li>
<li>Sanciones o descuentos por llegadas tarde o incumplimiento de normas internas.</li>
</ul>
<p>Una sola señal no define el caso. Se valora el conjunto y la forma real en que se ejecuta el contrato.</p>
<h2>Si eres contratista: obligaciones prácticas</h2>
<ul>
<li>Pagar tu planilla PILA cada mes sobre el 40% de tus ingresos netos. Ver la <a href="guia-pila-2026.html">guía de PILA</a>.</li>
<li>Emitir cuenta de cobro o factura según tu régimen tributario y conservar tus soportes.</li>
<li>Confirmar que el contratante te afilió a la ARL.</li>
<li>Declarar tus ingresos si superas los topes de la DIAN y tener en cuenta posibles retenciones en la fuente.</li>
<li>Apartar mensualmente un ahorro para vacaciones y ausencias, porque no se pagan.</li>
</ul>
<h2>Si eres empresa: cómo contratar contratistas con seguridad</h2>
<ul>
<li>Define por escrito el objeto, los entregables y el valor, sin horarios ni jefes directos.</li>
<li>Deja que el contratista decida cómo y cuándo trabajar, siempre que cumpla el resultado.</li>
<li>Exige la planilla de seguridad social pagada antes de cada pago de honorarios.</li>
<li>Evita que un contratista cubra funciones permanentes iguales a las de un empleado.</li>
</ul>
<h2>Qué hacer si crees que eres un empleado disfrazado</h2>
<p>Reúne evidencia: contrato, mensajes con órdenes, horarios, correos, pagos mensuales regulares. Consulta con un abogado laboral o con la inspección del Ministerio del Trabajo antes de renunciar o firmar un paz y salvo. Los derechos laborales prescriben en 3 años (CST, art. 488), así que el tiempo cuenta.</p>'''

ARTICULOS.append(dict(
    file="contratista-vs-empleado.html", tag="Tipos de contrato", calc="index.html#pila",
    h1="Contratista vs empleado: diferencias, contrato realidad y qué te corresponde",
    title="Contrato de prestación de servicios vs contrato de trabajo en Colombia | Calculadora Laboral",
    desc="Diferencias entre contratista y empleado en Colombia: prestaciones, seguridad social, elementos del contrato de trabajo, contrato realidad y señales de subordinación.",
    card="Tabla comparativa, elementos del contrato de trabajo, contrato realidad y obligaciones prácticas.",
    resumen=["El contrato de trabajo se define por actividad personal, subordinación y salario (CST, art. 23).",
             "El contratista no recibe cesantías, prima ni vacaciones, y paga su seguridad social por su cuenta.",
             "En la práctica prima la realidad sobre el nombre del contrato."],
    body=CVE,
    faq=[("¿Un contratista tiene derecho a prima y cesantías?", "No, salvo que se demuestre en un proceso que en realidad existió un contrato de trabajo (contrato realidad)."),
         ("¿Qué es la subordinación?", "Es la facultad del empleador de dar órdenes sobre el modo, tiempo o lugar de trabajo y de imponer reglamentos."),
         ("¿Quién paga la seguridad social del contratista?", "El propio contratista, sobre el 40% de sus ingresos netos. En riesgos IV y V la ARL la paga el contratante."),
         ("¿Cuánto tiempo tengo para reclamar si era un empleado?", "Generalmente 3 años desde que el derecho es exigible, con las particularidades que analice un abogado.")],
    fuentes=[("Código Sustantivo del Trabajo, arts. 22 a 24 y 488", None), ("Constitución Política de Colombia, art. 53 (primacía de la realidad)", None), ("Decreto 723 de 2013 (afiliación de contratistas a la ARL)", None), F_CST, F_MT, F_GN]))

# ------------------------------------------------------------------ CALENDARIO
CAL = f'''<p class="lead">Entre aportes, prestaciones y cambios de jornada, las obligaciones laborales se reparten a lo largo del año. Esta guía reúne las fechas que más se olvidan, tanto para empleados que quieren verificar que se las cumplan como para empleadores e independientes que necesitan organizarse.</p>
<h2>Cada mes</h2>
{tabla(["Qué", "Quién", "Fecha"], [
 ["Planilla PILA del mes anterior", "Independientes y empleadores", "Día hábil 2 a 16 del mes, según los dos últimos dígitos de la cédula o NIT"],
 ["Pago de la nómina", "Empleador", "Según el período pactado en el contrato (mensual o quincenal)"]])}
<p>El detalle de la fecha de pago de la PILA está en la <a href="guia-pila-2026.html">guía de PILA</a>.</p>
<h2>Calendario anual de prestaciones</h2>
{tabla(["Fecha", "Obligación", "Guía"], [
 ["31 de enero", "Pagar al trabajador los intereses sobre cesantías del año anterior", "<a href='cesantias-e-intereses.html'>Cesantías</a>"],
 ["14 de febrero", "Consignar las cesantías del año anterior en el fondo", "<a href='cesantias-e-intereses.html'>Cesantías</a>"],
 ["30 de abril", "Primera entrega de dotación (a quienes ganan hasta 2 SMMLV)", "<a href='salario-minimo-auxilio-transporte-2026.html'>Salario mínimo 2026</a>"],
 ["30 de junio", "Pagar la prima del primer semestre", "<a href='prima-de-servicios.html'>Prima</a>"],
 ["31 de agosto", "Segunda entrega de dotación", "<a href='salario-minimo-auxilio-transporte-2026.html'>Salario mínimo 2026</a>"],
 ["20 de diciembre", "Pagar la prima del segundo semestre y tercera entrega de dotación", "<a href='prima-de-servicios.html'>Prima</a>"]])}
<h2>Fechas de cambio normativo recientes</h2>
{tabla(["Fecha", "Cambio"], [
 ["25 de diciembre de 2025", "La jornada nocturna pasa a empezar a las 7 p. m. (Ley 2466 de 2025)."],
 ["1 de julio de 2026", "El recargo dominical y festivo sube al 90%."],
 ["15 de julio de 2026", "La jornada semanal baja a 42 horas (Ley 2101 de 2021)."],
 ["1 de julio de 2027", "El recargo dominical y festivo sube al 100%."]])}
<p>Mira cómo afectan al valor de la hora en la guía de <a href="horas-extra.html">horas extra y recargos</a>.</p>
<h2>Vacaciones y terminación del contrato</h2>
<ul>
<li><b>Vacaciones:</b> el empleador debe avisar con 15 días de anticipación la fecha en que las concederá. Ver <a href="vacaciones.html">vacaciones</a>.</li>
<li><b>Terminación:</b> la liquidación debe pagarse al terminar el contrato. Si hay demora, puede aplicar la indemnización moratoria. Ver <a href="como-se-calcula-la-liquidacion.html">liquidación</a>.</li>
<li><b>Contrato a término fijo:</b> si no se va a renovar, se debe avisar por escrito con al menos 30 días de anticipación al vencimiento (CST, art. 46).</li>
</ul>
<h2>Cómo usar este calendario</h2>
<p>Si eres empleado, anota las fechas de cesantías y prima y compáralas con tus pagos. Si eres independiente, programa tu PILA con una alerta antes de la fecha límite. Si eres empleador, provisiona cada mes las prestaciones para no tener que pagar un golpe grande en junio o diciembre. La calculadora de este sitio puede recordarte las fechas de pago de tu planilla.</p>'''

ARTICULOS.append(dict(
    file="calendario-obligaciones-laborales.html", tag="Calendario", calc="index.html#inicio",
    h1="Calendario de obligaciones laborales en Colombia: fechas clave de 2026",
    title="Calendario laboral 2026 en Colombia: cesantías, prima, PILA y dotación | Calculadora Laboral",
    desc="Todas las fechas clave del año: PILA mensual, intereses de cesantías, consignación del 14 de febrero, prima de junio y diciembre, dotación y cambios normativos.",
    card="PILA mensual, 31 de enero, 14 de febrero, 30 de junio, 20 de diciembre, dotación y cambios normativos.",
    resumen=["La PILA se paga mensualmente entre el día hábil 2 y el 16 según tu documento.",
             "Los intereses de cesantías vencen el 31 de enero y la consignación el 14 de febrero.",
             "La prima se paga el 30 de junio y el 20 de diciembre."],
    body=CAL,
    faq=[("¿Cuándo se pagan las cesantías?", "Se consignan en el fondo a más tardar el 14 de febrero del año siguiente al causado."),
         ("¿Cuándo se paga la prima?", "El 30 de junio y el 20 de diciembre."),
         ("¿Cuántas entregas de dotación hay al año?", "Tres: 30 de abril, 31 de agosto y 20 de diciembre, para quienes ganan hasta 2 SMMLV.")],
    fuentes=[("Código Sustantivo del Trabajo, arts. 46, 230, 249 y 306", None), ("Decreto 1990 de 2016 (plazos de pago de aportes)", None), F_CST, F_MT, F_GN]))

# ------------------------------------------------------------------ GLOSARIO
gl = [("AFP", "Administradora de Fondos de Pensiones. Entidad privada que administra tus aportes a pensión en el régimen de ahorro individual."),
      ("ARL", "Administradora de Riesgos Laborales. Cubre accidentes de trabajo y enfermedades laborales. Su tarifa depende del riesgo (I a V)."),
      ("BEPS", "Beneficios Económicos Periódicos. Mecanismo de ahorro para la vejez de personas con ingresos inferiores a un salario mínimo."),
      ("Caja de compensación", "Entidad que administra el subsidio familiar y servicios de recreación y vivienda. El empleador aporta 4% sobre la nómina."),
      ("Cesantías", "Prestación equivalente a un mes de salario por año trabajado, destinada a cubrir periodos de desempleo o fines de vivienda y estudio."),
      ("CST", "Código Sustantivo del Trabajo. Es la norma central del derecho laboral colombiano."),
      ("Contrato a término fijo", "Contrato con una fecha de terminación pactada. Su indemnización por despido se calcula con el tiempo que falta."),
      ("Dotación", "Calzado y vestido de labor que el empleador entrega tres veces al año a quienes ganan hasta 2 SMMLV."),
      ("EPS", "Entidad Promotora de Salud. Afilia y garantiza la atención en salud de sus afiliados."),
      ("Factor salarial", "Pago que constituye salario y entra en la base de prestaciones y aportes, como horas extra habituales y comisiones."),
      ("Fondo de Solidaridad Pensional", "Aporte adicional de 1% a 2% a pensión para quienes cotizan sobre 4 SMMLV o más."),
      ("IBC", "Ingreso Base de Cotización. Valor sobre el cual se calculan los aportes a seguridad social, con piso de 1 SMMLV y tope de 25."),
      ("Indemnización moratoria", "Sanción al empleador que no paga a tiempo salarios y prestaciones al terminar el contrato (CST, art. 65)."),
      ("Liquidación", "Cuenta final de lo que el empleador debe pagar al terminar el contrato."),
      ("PILA", "Planilla Integrada de Liquidación de Aportes. Es el sistema por el que se pagan los aportes a seguridad social."),
      ("Prima de servicios", "Pago de 30 días de salario por año, en dos cuotas semestrales."),
      ("Recargo", "Porcentaje adicional sobre el valor de la hora ordinaria por trabajo nocturno, dominical o festivo."),
      ("Salario integral", "Salario que incluye el factor prestacional. Se puede pactar desde 13 SMMLV y no genera cesantías ni prima por separado."),
      ("SMMLV", "Salario Mínimo Mensual Legal Vigente."),
      ("UGPP", "Unidad de Gestión Pensional y Parafiscales. Entidad que fiscaliza el pago de aportes a seguridad social."),
      ("Cotizante 76", "Tipo de cotizante de la PILA para independientes que trabajan por días o semanas y ganan menos de 1 SMMLV. Permite cotizar pensión de forma proporcional (Resolución 1529 de 2026)."),
      ("Paz y salvo", "Documento en que el trabajador declara que no se le adeuda nada. Conviene firmarlo solo después de verificar la liquidación."),
      ("Preaviso", "Aviso previo de terminación de un contrato a término fijo, de al menos 30 días.")]
GLO = '<p class="lead">Los términos laborales y de seguridad social suelen confundir. Aquí tienes las definiciones más usadas en las guías de este sitio, con enlaces a la explicación completa cuando existe.</p>' + \
      tabla(["Término", "Definición"], [[f"<b>{a}</b>", b] for a, b in sorted(gl, key=lambda x: x[0].lower())]) + \
      '<h2>Guías relacionadas</h2><ul><li><a href="guia-pila-2026.html">PILA para independientes</a></li><li><a href="pila-por-semanas-cotizante-76.html">PILA por semanas (cotizante 76)</a></li><li><a href="como-se-calcula-la-liquidacion.html">Liquidación laboral</a></li><li><a href="cesantias-e-intereses.html">Cesantías e intereses</a></li><li><a href="horas-extra.html">Horas extra y recargos</a></li></ul>'

ARTICULOS.append(dict(
    file="glosario-laboral.html", tag="Glosario", calc="index.html#inicio",
    h1="Glosario laboral colombiano: términos de seguridad social y nómina",
    title="Glosario laboral de Colombia: IBC, PILA, ARL, cesantías y más | Calculadora Laboral",
    desc="Definiciones claras de los términos laborales más usados en Colombia: IBC, PILA, ARL, UGPP, cesantías, prima, recargo, salario integral y más.",
    card="23 términos laborales y de seguridad social explicados con claridad.",
    resumen=None, body=GLO, faq=None,
    fuentes=[("Código Sustantivo del Trabajo", None), F_CST, F_UGPP, F_GN]))

# ==========================================================================================
# PÁGINAS DEL SITIO (acerca de, contacto, privacidad, términos)
# ==========================================================================================
SOBRE = f'''<p class="lead">{MARCA} es un proyecto independiente que reúne calculadoras y guías para entender los pagos laborales y de seguridad social en Colombia: PILA para independientes, liquidación, vacaciones, cesantías, prima, horas extra e indemnizaciones. Nació para resolver una necesidad práctica: poder verificar cuánto debes pagar o cuánto te deben pagar sin depender de hojas de cálculo improvisadas.</p>
<h2>Para quién es</h2>
<ul><li>Trabajadores independientes y contratistas que pagan su propia seguridad social.</li><li>Empleados que quieren revisar su desprendible, su liquidación o sus horas extra.</li><li>Pequeños empleadores que necesitan estimar el costo real de contratar.</li></ul>
<h2>Cómo elaboramos el contenido</h2>
<ul>
<li><b>Partimos de las normas.</b> Cada guía cita las normas en que se basa (Código Sustantivo del Trabajo, leyes, decretos) y enlaza a fuentes oficiales como el Ministerio del Trabajo, la UGPP y el Gestor Normativo de la Función Pública.</li>
<li><b>Los ejemplos se calculan con las mismas fórmulas que la calculadora.</b> Las cifras de las tablas no se escriben a mano: se generan con un programa que usa los valores del año, así que los ejemplos y la herramienta no se contradicen.</li>
<li><b>Mostramos el procedimiento, no solo el resultado.</b> Cada ejemplo muestra cada paso para que puedas replicarlo con tus propios datos.</li>
<li><b>Señalamos las zonas grises.</b> Cuando la ley admite interpretaciones distintas (por ejemplo, el pago del trabajo dominical ocasional frente al habitual), lo decimos y recomendamos confirmar el caso.</li>
</ul>
<h2>Convenciones de cálculo</h2>
{tabla(["Concepto", "Convención usada"], [
 ["Salario mínimo 2026", f"{f(S)} (Decreto 1469 de 2025)"], ["Auxilio de transporte 2026", f"{f(AUX)} (Decreto 1470 de 2025)"],
 ["Año para prestaciones", "360 días (12 meses de 30 días)"], ["Valor de un día de salario", "Salario mensual ÷ 30"],
 ["Valor de la hora ordinaria", "Salario mensual ÷ 210 (jornada de 42 horas semanales)"],
 ["IBC de independientes", "40% de los ingresos netos, entre 1 y 25 SMMLV"], ["Redondeo de la PILA", "Cada aporte se redondea hacia arriba al múltiplo de $100"]])}
<h2>Actualización y correcciones</h2>
<p>Cada guía muestra su fecha de actualización. Revisamos las cifras cuando cambia el salario mínimo y cuando se expiden normas que afectan los cálculos, como la reforma laboral de 2025. Si encuentras un error o una cifra desactualizada, <a href="contacto.html">escríbenos</a>: lo revisamos y, si corresponde, corregimos la guía.</p>
<h2>Independencia y publicidad</h2>
<p>El sitio se financia con publicidad de terceros, como Google AdSense, que se muestra en las guías. La publicidad no influye en el contenido, no recibimos pagos por mencionar productos o entidades y no vendemos asesoría. Más detalles en la <a href="privacidad.html">política de privacidad</a>.</p>
<h2>Límites de lo que ofrecemos</h2>
<p>La información es de referencia y los resultados de la calculadora son estimaciones. No somos un despacho de abogados ni una firma contable, y nada de lo publicado constituye asesoría jurídica, tributaria o financiera. Antes de pagar o firmar un documento, valida los valores con tu operador PILA, un contador, un abogado laboral o el Ministerio del Trabajo. Lee los <a href="terminos.html">términos y el descargo de responsabilidad</a>.</p>'''

CONTACTO = f'''<p class="lead">¿Encontraste un error, una cifra desactualizada o tienes una sugerencia de guía? Escríbenos.</p>
<h2>Correo de contacto</h2>
<p><a href="mailto:{CORREO}">{CORREO}</a></p>
<h2>Para qué puedes escribirnos</h2>
<ul>
<li>Reportar un error en una guía o en un cálculo. Indica el enlace de la página y qué cifra o texto consideras incorrecto.</li>
<li>Sugerir un tema o una función para la calculadora.</li>
<li>Consultas sobre la política de privacidad o sobre tus datos.</li>
<li>Temas de publicidad o colaboración editorial.</li>
</ul>
<h2>Lo que no podemos hacer</h2>
<p>No ofrecemos asesoría jurídica personalizada ni representación en procesos laborales. Para una situación específica, como un despido o una reclamación, consulta con un abogado laboral o con la inspección del trabajo del <a href="https://www.mintrabajo.gov.co/" rel="noopener" target="_blank">Ministerio del Trabajo</a>.</p>'''

PRIVACIDAD = f'''<p class="lead">Esta política explica qué información se trata cuando usas {MARCA} (https://{DOMINIO}), con qué fines y cuáles son tus derechos. Última actualización: {ACTUALIZADO}.</p>
<h2>Responsable</h2>
<p>El responsable del tratamiento es el equipo editorial de {MARCA}. Puedes contactarnos en <a href="mailto:{CORREO}">{CORREO}</a>.</p>
<h2>Datos de tus cálculos</h2>
<p>La calculadora no tiene cuentas de usuario ni base de datos propia. Los valores que ingresas, el historial de pagos, tus cobros y tus ajustes se guardan únicamente en el almacenamiento local de tu navegador (localStorage) y no se envían a nuestros servidores. Si borras los datos del navegador, se pierden; por eso la calculadora incluye una opción de copia de seguridad en Ajustes.</p>
<h2>Cookies y publicidad de Google</h2>
<p>Este sitio usa Google AdSense para mostrar anuncios. Google y sus socios publicitarios usan cookies y tecnologías similares para publicar anuncios basados en tus visitas anteriores a este y otros sitios web. Estos son los puntos clave:</p>
<ul>
<li>Google, como proveedor externo, utiliza cookies para publicar anuncios en este sitio.</li>
<li>El uso de cookies de publicidad permite a Google y a sus socios mostrar anuncios basados en tu navegación por este y otros sitios de Internet.</li>
<li>Puedes inhabilitar la publicidad personalizada en la <a href="https://adssettings.google.com" rel="noopener" target="_blank">configuración de anuncios de Google</a>.</li>
<li>También puedes consultar <a href="https://www.aboutads.info" rel="noopener" target="_blank">aboutads.info</a> para inhabilitar cookies de proveedores externos y conocer cómo <a href="https://policies.google.com/technologies/partner-sites" rel="noopener" target="_blank">Google usa los datos de los sitios que usan sus servicios</a>.</li>
</ul>
{ANALITICA}<h2>Tipografías de Google Fonts</h2>
<p>Las tipografías se cargan desde Google Fonts. Al visitar el sitio, tu navegador se conecta a servidores de Google, que pueden registrar tu dirección IP como parte del servicio.</p>
<h2>Datos que nos envías por correo</h2>
<p>Si nos escribes, usamos tu correo y el contenido de tu mensaje solo para responderte y mejorar el sitio. No los vendemos ni los compartimos con terceros.</p>
<h2>Tus derechos</h2>
<p>De acuerdo con la Ley 1581 de 2012 de protección de datos personales de Colombia, puedes conocer, actualizar, rectificar y solicitar la supresión de tus datos, y revocar la autorización. Para ejercer estos derechos, escríbenos a <a href="mailto:{CORREO}">{CORREO}</a>. También puedes acudir a la Superintendencia de Industria y Comercio, autoridad de protección de datos.</p>
<h2>Menores de edad</h2>
<p>El sitio no está dirigido a menores de edad y no recopilamos intencionalmente datos de ellos.</p>
<h2>Cambios en esta política</h2>
<p>Podemos actualizar esta política cuando cambien el sitio o la normativa. La fecha de la última actualización aparece al inicio.</p>'''

TERMINOS = f'''<p class="lead">Al usar {MARCA} aceptas estos términos. Última actualización: {ACTUALIZADO}.</p>
<h2>Naturaleza informativa</h2>
<p>Las guías y la calculadora son una referencia basada en la legislación laboral y de seguridad social vigente en Colombia en 2026. Los resultados son estimaciones matemáticas orientativas y no constituyen un dictamen jurídico, contable, tributario ni financiero.</p>
<h2>Validación profesional</h2>
<p>Antes de realizar pagos en un operador PILA, firmar acuerdos de liquidación, tomar decisiones contractuales o iniciar reclamaciones, debes validar los valores con un contador, un abogado laboral o directamente ante las entidades competentes (Ministerio del Trabajo, UGPP o tu operador autorizado).</p>
<h2>Exactitud y vigencia</h2>
<p>Hacemos un esfuerzo razonable por mantener la información correcta y actualizada, pero las normas cambian, pueden ser interpretadas de formas distintas y cada caso tiene particularidades. No garantizamos que el contenido esté libre de errores u omisiones.</p>
<h2>Limitación de responsabilidad</h2>
<p>Los responsables del sitio no asumen responsabilidad por decisiones tomadas con base en el contenido o en los cálculos automatizados, ni por perjuicios derivados de su uso, en la medida permitida por la ley.</p>
<h2>Propiedad intelectual</h2>
<p>Los textos, tablas y el diseño del sitio son propiedad de sus autores. Puedes citar fragmentos breves con un enlace visible a la página de origen. No está permitido copiar guías completas ni presentarlas como propias.</p>
<h2>Enlaces a sitios externos</h2>
<p>Enlazamos a páginas oficiales y de terceros para ampliar la información. No controlamos su contenido y no somos responsables por él.</p>
<h2>Ley aplicable</h2>
<p>Estos términos se rigen por las leyes de la República de Colombia.</p>
<h2>Contacto</h2>
<p>Para cualquier duda sobre estos términos, escríbenos a <a href="mailto:{CORREO}">{CORREO}</a>.</p>'''

PAGINAS_FIJAS = [
    ("sobre-nosotros.html", "Sobre el sitio y metodología", "Sobre el sitio, metodología y fuentes", f"Sobre {MARCA}: cómo elaboramos las guías, convenciones de cálculo, fuentes oficiales, política de actualización e independencia editorial.", SOBRE),
    ("contacto.html", "Contacto", "Contacto", f"Escríbenos para reportar un error, sugerir un tema o consultar sobre privacidad en {MARCA}.", CONTACTO),
    ("privacidad.html", "Política de privacidad", "Política de privacidad", f"Política de privacidad de {MARCA}: datos locales, cookies de Google AdSense, Google Fonts y derechos del titular según la Ley 1581 de 2012.", PRIVACIDAD),
    ("terminos.html", "Términos y descargo de responsabilidad", "Términos y descargo de responsabilidad", f"Términos de uso y descargo de responsabilidad de {MARCA}: naturaleza informativa, validación profesional y limitación de responsabilidad.", TERMINOS),
]

# ==========================================================================================
# CONSTRUCCIÓN
# ==========================================================================================
def esc(s): return html.escape(s, quote=True)

def cards(items):
    return "".join(f'<a class="card" href="{a["file"]}"><small>{a["tag"]}</small><b>{a["h1"]}</b><span>{a["card"]}</span></a>' for a in items)

FOOT = "".join(f'<a href="{a["file"]}">{t}</a>' for a, t in [(x, x["h1"].split(":")[0].split(" en Colombia")[0][:48]) for x in ARTICULOS[:6]])

def render(file, title, desc, h1, tag, body, calc="index.html#inicio", resumen=None, faq=None, fuentes=None, article=True, more_from=None):
    body, toc = prep(body)
    fq, fq_ld = faq_html(faq)
    palabras = len(re.sub(r"<[^>]+>", " ", body + fq).split())
    mins = max(2, round(palabras / 200))
    res = ""
    if resumen:
        res = '<div class="box"><p><b>En breve</b></p><ul>' + "".join(f"<li>{r}</li>" for r in resumen) + "</ul></div>"
    ld = []
    if article:
        ld.append({"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc, "inLanguage": "es-CO",
                   "dateModified": HOY, "datePublished": HOY, "mainEntityOfPage": f"https://{DOMINIO}/{file}",
                   "author": {"@type": "Organization", "name": MARCA}, "publisher": {"@type": "Organization", "name": MARCA}})
    if fq_ld: ld.append(fq_ld)
    jsonld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    norma = (f' · Norma base: {fuentes[0][0]} (<a href="#fuentes">ver fuentes</a>)' if fuentes else "")
    metaline = (f'<p class="meta">Revisado el {REVISADO}{norma} · {mins} min de lectura · Elaborado por el equipo editorial de {MARCA} (<a href="sobre-nosotros.html">cómo trabajamos</a>)</p>' if article
                else f'<p class="meta">Actualizado en {ACTUALIZADO}</p>')
    cta = (f'<div class="cta"><p><b>¿Quieres calcularlo con tus propios valores?</b></p><a class="btn" href="{calc}">Abrir la calculadora interactiva</a></div>' if article else "")
    disc = ('<p class="meta">Información de referencia basada en la normativa vigente en 2026. Es una estimación orientativa y no reemplaza la asesoría de un contador o abogado laboral. Verifica los valores en tu operador PILA, ante la UGPP o el Ministerio del Trabajo.</p>' if article else "")
    more = ""
    if more_from:
        more = '<h2>Sigue leyendo</h2>' + cards(more_from) + '<p><a href="blog.html">← Ver todas las guías</a> · <a href="index.html#inicio">Volver a la calculadora</a></p>'
    out = (TPL.replace("@ADS@", ADS if article else "").replace("@GA@", GA).replace("@JSONLD@", jsonld).replace("@METALINE@", metaline).replace("@CTA@", cta).replace("@DISC@", disc)
              .replace("@RESUMEN@", res).replace("@TOC@", toc).replace("@BODY@", body).replace("@FAQ@", fq).replace("@FUENTES@", fuentes_html(fuentes) if fuentes else "")
              .replace("@MORE@", more).replace("@FOOTGUIAS@", FOOT + '<a href="blog.html">Ver todas las guías</a>')
              .replace("@TITLE@", esc(title)).replace("@DESC@", esc(desc)).replace("@FILE@", file).replace("@DOM@", DOMINIO)
              .replace("@H1@", h1).replace("@TAG@", tag).replace("@CALC@", calc).replace("@MARCA@", MARCA))
    out = out.replace('<meta property="og:type" content="article">', f'<meta property="og:type" content="{"article" if article else "website"}">')
    with open(os.path.join(SALIDA, file), "w", encoding="utf-8") as fh:
        fh.write(out)
    return mins


os.makedirs(SALIDA, exist_ok=True)
resumen_lect = {}
for i, a in enumerate(ARTICULOS):
    otros = [x for x in ARTICULOS if x is not a]
    k = ARTICULOS.index(a)
    rel = [ARTICULOS[(k + d) % len(ARTICULOS)] for d in (1, 2, 3)]
    resumen_lect[a["file"]] = render(a["file"], a["title"], a["desc"], a["h1"], a["tag"], a["body"], a["calc"], a.get("resumen"), a.get("faq"), a.get("fuentes"), True, rel)

BLOGP = ('<p class="lead">Guías claras y con ejemplos numéricos de 2026 sobre seguridad social, liquidación, prestaciones, horas extra e indemnizaciones en Colombia. Cada guía cita las normas en que se basa y enlaza a la calculadora para que pruebes tus propios valores.</p>'
         + '<h2>Todas las guías</h2>' + cards(ARTICULOS))
render("blog.html", "Guías laborales de Colombia 2026: PILA, liquidación, cesantías y horas extra | Calculadora Laboral",
       "Guías con ejemplos numéricos de 2026 sobre PILA, liquidación, cesantías, prima, vacaciones, horas extra, indemnización y costo de un empleado en Colombia.",
       "Guías laborales y de seguridad social", "Guías", BLOGP, article=True)

for fl, tg, h1, ds, bd in PAGINAS_FIJAS:
    render(fl, f"{h1} | {MARCA}", ds, h1, tg, bd, article=False)

# sitemap y robots
PAGINAS = ["index.html", "blog.html"] + [a["file"] for a in ARTICULOS] + [p[0] for p in PAGINAS_FIJAS]
with open(os.path.join(SALIDA, "sitemap.xml"), "w", encoding="utf-8") as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p_ in PAGINAS:
        pr_ = "1.0" if p_ == "index.html" else ("0.8" if p_ == "blog.html" or p_ in [a["file"] for a in ARTICULOS] else "0.3")
        fh.write(f"  <url><loc>https://{DOMINIO}/{'' if p_ == 'index.html' else p_}</loc><lastmod>{HOY}</lastmod><priority>{pr_}</priority></url>\n")
    fh.write("</urlset>\n")
with open(os.path.join(SALIDA, "robots.txt"), "w", encoding="utf-8") as fh:
    fh.write(f"User-agent: *\nAllow: /\n\nSitemap: https://{DOMINIO}/sitemap.xml\n")

print("Listo:", len(PAGINAS) - 1, "páginas + sitemap.xml + robots.txt en", os.path.abspath(SALIDA))
for k, v in resumen_lect.items(): print(f"  {k:48s} ~{v} min")
