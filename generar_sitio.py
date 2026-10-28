#!/usr/bin/env python3
"""
Generador del blog de la Calculadora Laboral.

Todo el blog vive en este archivo: la plantilla (cabecera, pie, estilos) y el texto de cada
artículo. Al ejecutarlo se crean las páginas HTML independientes, listas para subir:
    horas-extra.html, indemnizacion.html, guia-pila-2026.html,
    como-se-calcula-la-liquidacion.html, blog.html y sitemap.xml

Uso:  python3 generar_sitio.py

Para cambiar el pie o los estilos: edita TPL.
Para cambiar un texto: edita la variable del artículo (HEX, IND, PILA, LIQ).
Para agregar un artículo: crea su cuerpo, añádelo a ART y a la lista PAGINAS del final.
"""
import os

# ====== CONFIGURACIÓN ======
DOMINIO = "calculadoralaboralcolombia.online"   # sin https:// y sin barra final
SALIDA = "."             # carpeta donde se escriben los archivos
# ===========================

import math, datetime
S = 1750905; AUX = 249095
f = lambda n: "$ " + f"{round(n):,}".replace(",", ".")
up = lambda x: math.ceil(round(x/100, 6))*100

def pila(h, c=0, arl=0.00522):
    ibcb = (h-c)*.4; ibc = round(min(max(ibcb, S), 25*S))
    s, p, a = up(ibc*.125), up(ibc*.16), up(ibc*arl)
    return ibcb, ibc, s, p, a, s+p+a
e1 = pila(5_000_000); e2 = pila(3_000_000)
bc = 3_500_000+AUX; ces = bc*180/360; inte = ces*180*.12/360; pr = bc*180/360; vac = 3_500_000/30*7.5
tot = ces+inte+pr+vac
i_indef = 3_500_000/30*60; i_fijo = 3_500_000/30*90

TPL = r'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>@TITLE@</title>
<meta name="description" content="@DESC@">
<link rel="canonical" href="https://@DOM@/@FILE@">
<meta property="og:type" content="article"><meta property="og:title" content="@TITLE@"><meta property="og:description" content="@DESC@"><meta property="og:url" content="https://@DOM@/@FILE@">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧮</text></svg>">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3761150056608968" crossorigin="anonymous"></script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Figtree:wght@400..700&display=swap">
<style>
:root{--bg:#F3F1FA;--surface:#fff;--ink:#171437;--muted:#5E5B80;--line:#E2DFF0;--accent:#4338CA;--accent-ink:#fff;--soft:#E8E6FB;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--bg:#0E0C20;--surface:#171433;--ink:#ECEAFB;--muted:#9E9BC4;--line:#2B2850;--accent:#9C93FF;--accent-ink:#0E0C20;--soft:#25214F;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 Figtree,system-ui,sans-serif;padding:env(safe-area-inset-top) 0 env(safe-area-inset-bottom)}
header{border-bottom:1px solid var(--line);background:var(--surface)}
.in{max-width:46rem;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left))}
header .in{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding-top:.8rem;padding-bottom:.8rem}
.brand{font:700 1.05rem "Bricolage Grotesque",Figtree,sans-serif;color:var(--ink);text-decoration:none}
.btn{display:inline-block;padding:.6rem 1.1rem;border-radius:10px;background:var(--accent);color:var(--accent-ink);font-weight:600;text-decoration:none}
.btn.s{padding:.4rem .8rem;font-size:.88rem}
h1{font:700 clamp(1.7rem,5vw,2.4rem)/1.15 "Bricolage Grotesque",Figtree,sans-serif;margin:1.6rem 0 .4rem;text-wrap:balance}
h2{font:700 1.4rem/1.25 "Bricolage Grotesque",Figtree,sans-serif;margin:2rem 0 .4rem}
h3{font-size:1.05rem;margin:1.2rem 0 .2rem}
p,li{max-width:70ch}.meta{color:var(--muted);font-size:.88rem}
a{color:var(--accent)}
.box{background:var(--surface);border:1px solid var(--line);border-left:5px solid var(--accent);border-radius:12px;padding:1rem 1.2rem;margin:1.2rem 0}
.box p{margin:.3rem 0}
.cta{background:var(--soft);border-radius:16px;padding:1.2rem;margin:2rem 0;text-align:center}
.cta p{margin:0 auto .8rem}
table{border-collapse:collapse;width:100%;font-size:.92rem;margin:.6rem 0}th,td{border-bottom:1px solid var(--line);padding:.4rem .5rem;text-align:left}td.n,th.n{text-align:right;white-space:nowrap}
.tw{overflow-x:auto}
footer{border-top:1px solid var(--line);margin-top:2.5rem;padding:1.2rem 0 2rem;font-size:.82rem;color:var(--muted)}
footer a{margin-right:1rem}
</style></head><body>
<header><div class="in"><a class="brand" href="index.html">Calculadora Laboral Colombia</a><a class="btn s" href="@CALC@">Ir a la calculadora</a></div></header>
<main class="in"><article>
<p class="meta" style="margin-top:1.2rem">Guía · actualizada en octubre de 2026</p>
<h1>@H1@</h1>
@BODY@
<div class="cta"><p><b>¿Quieres calcularlo con tus propios valores?</b></p><a class="btn" href="@CALC@">Ir a la calculadora interactiva</a></div>
<p class="meta">Información de referencia basada en la normativa vigente en 2026. Es una estimación orientativa y no reemplaza la asesoría de un contador o abogado laboral. Verifica los valores en tu operador PILA o ante el Ministerio del Trabajo.</p>
</article></main>
<footer><div class="in"><a href="index.html">Inicio</a><a href="guia-pila-2026.html">Guía PILA 2026</a><a href="como-se-calcula-la-liquidacion.html">Guía de liquidación</a><a href="index.html?ver=privacidad">Privacidad</a><a href="index.html?ver=terminos">Términos</a><a href="index.html?ver=contacto">Contacto</a></div></footer>
</body></html>'''

CTA = '<div class="cta"><p><b>Prueba el cálculo con tus cifras</b></p><a class="btn" href="@CALC@">Ir a la calculadora interactiva</a></div>'

def ex(t, r):
    ib, ibc, s, p, a, tot_ = r
    return (f'<table><tbody><tr><td>IBC (40%, con piso de 1 SMMLV)</td><td class="n">{f(ibc)}</td></tr>'
            f'<tr><td>Salud 12,5%</td><td class="n">{f(s)}</td></tr><tr><td>Pensión 16%</td><td class="n">{f(p)}</td></tr>'
            f'<tr><td>ARL riesgo I (0,522%)</td><td class="n">{f(a)}</td></tr><tr><th>Total a pagar</th><th class="n">{f(tot_)}</th></tr></tbody></table>')

dias = [("00 a 07",2),("08 a 14",3),("15 a 21",4),("22 a 28",5),("29 a 35",6),("36 a 42",7),("43 a 49",8),("50 a 56",9),("57 a 63",10),("64 a 69",11),("70 a 75",12),("76 a 81",13),("82 a 87",14),("88 a 93",15),("94 a 99",16)]
tabla = '<div class="tw"><table><thead><tr><th>Últimos 2 dígitos</th><th class="n">Día hábil de pago</th></tr></thead><tbody>' + "".join(f'<tr><td>{a}</td><td class="n">{b}</td></tr>' for a, b in dias) + '</tbody></table></div>'

PILA = f'''<p>Si trabajas por cuenta propia o con contrato de prestación de servicios, eres tú quien paga mes a mes tu salud, tu pensión y tu riesgos laborales a través de la planilla PILA. Esta guía explica cómo se calcula cada aporte, con ejemplos reales con los valores de 2026: salario mínimo (SMMLV) de {f(S)}.</p>
<h2>Quién debe cotizar como independiente</h2>
<p>Cotizan los independientes y contratistas con ingresos mensuales iguales o superiores a 1 SMMLV. Si tus ingresos netos son menores, la ley no te obliga a cotizar como independiente, aunque puedes consultar con tu EPS o contador otras opciones de afiliación.</p>
<h2>Paso 1: calcula tus ingresos netos del mes</h2>
<p>Parte de lo que facturaste en el mes, sin IVA. Si tienes costos y gastos que puedes soportar (por ejemplo herramientas de trabajo o arriendo de oficina), se restan antes de seguir. La UGPP puede pedirte soportes, por eso conviene guardar facturas y cuentas de cobro.</p>
<h2>Paso 2: obtén tu IBC (el 40%)</h2>
<p>El ingreso base de cotización (IBC) es el 40% de tus ingresos netos mensuales. Tiene un piso de 1 SMMLV ({f(S)}) y un tope de 25 SMMLV ({f(25*S)}). Si el 40% queda por debajo del piso, se cotiza sobre el mínimo.</p>
<h2>Paso 3: aplica los porcentajes</h2>
<ul><li><b>Salud:</b> 12,5% del IBC.</li><li><b>Pensión:</b> 16% del IBC.</li><li><b>Fondo de Solidaridad Pensional:</b> 1% desde 4 SMMLV de IBC, y sube gradualmente hasta 2% desde 20 SMMLV.</li><li><b>ARL:</b> según el riesgo de tu actividad. Riesgo I es 0,522% y llega a 6,96% en riesgo V. En riesgos IV y V la paga el contratante.</li><li><b>Caja de compensación:</b> opcional, 0,6% o 2% si te afilias.</li></ul>
<h2>Paso 4: redondea y suma</h2>
<p>La PILA redondea cada aporte hacia arriba al múltiplo de $100 más cercano. La suma de todos los aportes es el valor de tu planilla.</p>
<h2>Ejemplo 1: honorarios de {f(5_000_000)}</h2>
<p>El 40% de $ 5.000.000 es $ 2.000.000, que supera el piso. Con ARL de riesgo I y sin caja:</p>
{ex(1, e1)}
<h2>Ejemplo 2: honorarios de {f(3_000_000)} (aplica el piso)</h2>
<p>El 40% de $ 3.000.000 es $ 1.200.000, menor que 1 SMMLV. Se cotiza sobre {f(S)}:</p>
{ex(2, e2)}
{CTA}
<h2>¿Cuándo vence tu planilla?</h2>
<p>Pagas mes vencido: en octubre pagas el período de septiembre. El día límite depende de los dos últimos dígitos de tu cédula o NIT (Decreto 1990 de 2016) y se cuenta en días hábiles del mes siguiente:</p>
{tabla}
<p class="meta">Contados de lunes a viernes sin festivos. Confirma la fecha exacta en tu operador PILA.</p>
<h2>Errores frecuentes</h2>
<ul><li>Cotizar sobre el 40% de lo recibido y olvidar que los costos solo se restan si están soportados.</li><li>Dejar de pagar un mes porque no hubo ingresos, sin informar la novedad correspondiente al operador.</li><li>Pagar la ARL de riesgo IV o V cuando le corresponde al contratante.</li><li>Cotizar un IBC distinto al de tus ingresos reales: la UGPP puede cruzar la información.</li></ul>
<h2>Normas de referencia</h2>
<p>Ley 100 de 1993; Ley 797 de 2003 (Fondo de Solidaridad Pensional); Ley 1955 de 2019, art. 244 (IBC del 40%); Decreto 723 de 2013 (ARL de contratistas); Decreto 1990 de 2016 (plazos de pago). Verifica su vigencia, pues pueden ser modificadas.</p>'''

LIQ = f'''<p>Cuando termina un contrato laboral, el empleador debe liquidar lo que le adeuda al trabajador. Esta guía explica qué conceptos incluye, cómo se calcula cada uno y muestra un ejemplo numérico con los valores de 2026: SMMLV de {f(S)} y auxilio de transporte de {f(AUX)}.</p>
<h2>Qué incluye la liquidación</h2>
<ul><li><b>Cesantías:</b> un mes de salario por año de servicio (CST, art. 249).</li><li><b>Intereses sobre cesantías:</b> 12% anual sobre las cesantías causadas (Ley 52 de 1975).</li><li><b>Prima de servicios:</b> 30 días de salario por año, pagados por semestres (CST, art. 306).</li><li><b>Vacaciones pendientes:</b> 15 días hábiles por año trabajado (CST, art. 186).</li><li><b>Salario pendiente:</b> días trabajados que aún no se han pagado.</li><li><b>Indemnización:</b> solo si el despido es sin justa causa (CST, art. 64).</li></ul>
<h2>Cómo se calcula cada concepto</h2>
<p>Los cálculos usan el año de 360 días. La base de cesantías y prima es el salario más el auxilio de transporte (si lo recibes: aplica hasta 2 SMMLV). La base de vacaciones es el salario sin auxilio.</p>
<ul><li>Cesantías = base × días trabajados en el año ÷ 360.</li><li>Intereses = cesantías × días × 12% ÷ 360.</li><li>Prima = base × días del semestre ÷ 360.</li><li>Vacaciones = (salario ÷ 30) × (15 × días ÷ 360 − días ya disfrutados).</li></ul>
<h2>Ejemplo: contrato del 1 de enero al 30 de junio de 2026</h2>
<p>Salario de {f(3_500_000)} más auxilio de transporte: la base es {f(bc)}. Son 180 días de servicio.</p>
<div class="tw"><table><tbody><tr><td>Cesantías (180 días)</td><td class="n">{f(ces)}</td></tr><tr><td>Intereses sobre cesantías</td><td class="n">{f(inte)}</td></tr><tr><td>Prima de servicios (180 días)</td><td class="n">{f(pr)}</td></tr><tr><td>Vacaciones (7,5 días hábiles)</td><td class="n">{f(vac)}</td></tr><tr><th>Total estimado</th><th class="n">{f(tot)}</th></tr></tbody></table></div>
{CTA}
<h2>Indemnización por despido sin justa causa</h2>
<h3>Contrato a término indefinido</h3>
<p>Si el salario es menor a 10 SMMLV: 30 días de salario por el primer año y 20 días adicionales por cada año siguiente (proporcional por fracciones). Con 10 SMMLV o más: 20 días el primer año y 15 por cada año adicional. Ejemplo: salario de {f(3_500_000)} y 900 días de servicio (2,5 años) → 30 + 20 × 1,5 = 60 días de salario = <b>{f(i_indef)}</b>.</p>
<h3>Contrato a término fijo</h3>
<p>Corresponde al valor de los salarios del tiempo que falta para cumplir el plazo pactado. Ejemplo: faltan 90 días y el salario es {f(3_500_000)} → <b>{f(i_fijo)}</b>. En contratos por duración de obra o labor, el artículo 64 fija un mínimo de 15 días de salario.</p>
<h2>Plazos y mora</h2>
<p>La liquidación debe pagarse al terminar el contrato. Si el empleador no lo hace, puede aplicar indemnización moratoria (CST, art. 65). Antes de firmar un acuerdo de liquidación o un paz y salvo, valida las cifras con un abogado laboral o el Ministerio del Trabajo.</p>
<h2>Lo que este estimado no incluye</h2>
<p>No descuenta préstamos, libranzas ni retención en la fuente, y no considera factores salariales variables (comisiones, horas extra) que modifican la base: si los tienes, usa el promedio que corresponda según tu caso.</p>'''

import re
TPL = TPL.replace('<a class="brand" href="index.html">Calculadora Laboral Colombia</a><a class="btn s" href="@CALC@">Ir a la calculadora</a>',
  '<a class="brand" href="index.html">Calculadora Laboral Colombia</a><nav><a href="index.html#inicio">Inicio</a><a href="blog.html">Blog</a><a class="btn s" href="@CALC@">Ir a la calculadora</a></nav>')
TPL = TPL.replace("footer{", "nav a:not(.btn){margin-right:.9rem;text-decoration:none;color:var(--muted);font-size:.9rem}nav a:not(.btn):hover{color:var(--accent)}\n.card{display:block;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:1rem 1.2rem;margin:.7rem 0;text-decoration:none;color:var(--ink)}.card:hover{border-color:var(--accent)}.card small{color:var(--accent);font-weight:600}.card b{display:block;font-size:1.05rem}.card span{color:var(--muted);font-size:.9rem}\nfooter{", 1)
TPL = TPL.replace('<p class="meta" style="margin-top:1.2rem">Guía · actualizada en octubre de 2026</p>',
  '<p class="meta" style="margin-top:1.2rem"><a href="index.html#inicio">Inicio</a> › <a href="blog.html">Blog</a> · actualizado en octubre de 2026</p>')
TPL = TPL.replace('<p class="meta">Información de referencia', '@MORE@\n<p class="meta">Información de referencia')
TPL = TPL.replace('<a href="guia-pila-2026.html">Guía PILA 2026</a>', '<a href="blog.html">Blog</a><a href="guia-pila-2026.html">Guía PILA 2026</a>')

ART = [
 ("horas-extra.html", "Jornada laboral 2026", "Cómo calcular las horas extra y recargos", "Tarifas diurnas, nocturnas y dominicales con la jornada de 42 horas y el recargo dominical del 90%."),
 ("indemnizacion.html", "Estabilidad laboral", "Indemnización por despido sin justa causa", "Cómo se calcula en contratos a término indefinido, fijo y por obra o labor."),
 ("guia-pila-2026.html", "Guía 2026", "PILA para independientes, paso a paso", "Cómo calcular tu IBC, salud, pensión y ARL, con ejemplos numéricos y fechas de pago."),
 ("como-se-calcula-la-liquidacion.html", "Guía 2026", "Cómo se calcula tu liquidación laboral", "Cesantías, intereses, prima, vacaciones e indemnización, con fórmulas y un ejemplo."),
]
def cards(skip=None):
    return "".join(f'<a class="card" href="{u}"><small>{t}</small><b>{n}</b><span>{d}</span></a>' for u, t, n, d in ART if u != skip)

hora = 3_500_000/210
fac = [("Hora extra diurna", .25, 1.25), ("Hora extra nocturna", .75, 1.75), ("Recargo nocturno", .35, 1.35), ("Dominical o festivo diurno", .90, 1.90),
       ("Nocturno en dominical o festivo", 1.25, 2.25), ("Extra diurna en dominical o festivo", 1.15, 2.15), ("Extra nocturna en dominical o festivo", 1.65, 2.65)]
tabh = '<div class="tw"><table><thead><tr><th>Tipo de hora</th><th class="n">Recargo</th><th class="n">Factor</th><th class="n">Valor con recargo</th></tr></thead><tbody>' + "".join(
    f'<tr><td>{a}</td><td class="n">{round(b*100)}%</td><td class="n">{str(c).replace(".", ",")}</td><td class="n">{f(hora*c)}</td></tr>' for a, b, c in fac) + '</tbody></table></div>'
HEX = f'''<p>En Colombia, el trabajo suplementario, el nocturno y el realizado en domingos o festivos se pagan con recargos sobre el valor de la hora ordinaria. Esta guía explica cómo se calcula cada uno con las reglas de 2026: jornada de 42 horas semanales y recargo dominical y festivo del 90%.</p>
<h2>Paso 1: el valor de la hora ordinaria</h2>
<p>Con la jornada de 42 horas semanales, el mes se toma de 210 horas ordinarias (42 horas ÷ 6 días × 30 días). El valor de la hora es el salario mensual dividido entre 210. Con un salario de {f(3_500_000)}, cada hora vale <b>{f(hora)}</b>.</p>
<h2>Paso 2: identifica el tipo de hora</h2>
<ul><li><b>Hora extra diurna:</b> la que excede la jornada entre las 6 a. m. y las 7 p. m. Recargo del 25%.</li><li><b>Hora extra nocturna:</b> la que excede la jornada entre las 7 p. m. y las 6 a. m. Recargo del 75%.</li><li><b>Recargo nocturno:</b> hora ordinaria trabajada de noche. Recargo del 35%.</li><li><b>Dominical o festivo:</b> trabajo en día de descanso obligatorio. Recargo del 90% en 2026, que sube de forma gradual hasta el 100% en 2027.</li></ul>
<p>Los recargos se suman cuando coinciden: por ejemplo, una hora nocturna en domingo suma el 35% y el 90%.</p>
<h2>Paso 3: valor de cada hora con recargo (salario de {f(3_500_000)})</h2>
{tabh}
<p class="meta">Factor = 1 + recargo. Valor = valor de la hora ordinaria × factor.</p>
{CTA.replace("@CALC@", "index.html#hex")}
<h2>Ejemplo</h2>
<p>Un trabajador con salario de {f(3_500_000)} labora en el mes 8 horas extra diurnas y 4 horas extra nocturnas. Las extras se pagan completas: 8 × {f(hora*1.25)} = <b>{f(8*hora*1.25)}</b> y 4 × {f(hora*1.75)} = <b>{f(4*hora*1.75)}</b>. Total adicional al salario: <b>{f(8*hora*1.25 + 4*hora*1.75)}</b>.</p>
<h2>Límites y reglas importantes</h2>
<ul><li>No se pueden trabajar más de 2 horas extra al día ni más de 12 a la semana.</li><li>Las horas extra requieren autorización del empleador o del Ministerio del Trabajo, según el caso.</li><li>Las horas extra, los recargos y las comisiones son factor salarial: cuentan para los aportes a seguridad social, la prima y las cesantías.</li><li>Los cargos de dirección, confianza y manejo no tienen derecho a horas extra.</li></ul>
<h2>Una precisión sobre el recargo dominical</h2>
<p>La calculadora del sitio paga en los recargos solo el porcentaje adicional, porque supone que tu salario mensual ya cubre la hora ordinaria. En el trabajo dominical y festivo, muchas empresas pagan la hora completa más el recargo. Confirma con tu empleador, tu contrato o un abogado laboral cuál se aplica en tu caso.</p>
<h2>Normas de referencia</h2>
<p>Código Sustantivo del Trabajo, arts. 159, 160, 168 y 179; Ley 2101 de 2021 (reducción de la jornada a 42 horas); Ley 2466 de 2025 (reforma laboral: horario nocturno desde las 7 p. m. y recargo dominical gradual). Verifica su vigencia.</p>'''

IND = f'''<p>La indemnización por despido sin justa causa es el pago que debe hacer el empleador cuando termina el contrato de forma unilateral y sin una causa legal. Se regula en el artículo 64 del Código Sustantivo del Trabajo y depende del tipo de contrato, del salario y del tiempo de servicio.</p>
<h2>Cuándo hay derecho a indemnización</h2>
<p>Cuando el empleador termina el contrato sin invocar una justa causa de las previstas en el artículo 62 del CST, o cuando la causa invocada no se logra demostrar. No hay indemnización si renuncias, si hay mutuo acuerdo o si vence el plazo de un contrato fijo con preaviso.</p>
<h2>Contrato a término indefinido</h2>
<ul><li><b>Salario menor a 10 SMMLV:</b> 30 días de salario por el primer año y 20 días por cada año adicional, proporcional por fracciones.</li><li><b>Salario de 10 SMMLV o más:</b> 20 días por el primer año y 15 días por cada año adicional.</li></ul>
<p>Ejemplo 1: salario de {f(3_500_000)} y 900 días de servicio (2,5 años). Son 30 + 20 × 1,5 = 60 días de salario. Como el valor de un día es {f(3_500_000/30)}, la indemnización es <b>{f(i_indef)}</b>.</p>
<p>Ejemplo 2: salario de {f(20_000_000)} (más de 10 SMMLV) y 720 días de servicio (2 años). Son 20 + 15 × 1 = 35 días de salario, es decir <b>{f(20_000_000/30*35)}</b>.</p>
<h2>Contrato a término fijo</h2>
<p>La indemnización es el valor de los salarios del tiempo que falta para cumplir el plazo pactado. Ejemplo: salario de {f(3_500_000)} y 90 días restantes → 90 × {f(3_500_000/30)} = <b>{f(i_fijo)}</b>.</p>
<h2>Contrato por obra o labor</h2>
<p>Se pagan los salarios del tiempo que falte para terminar la obra o labor, y la indemnización no puede ser inferior a 15 días de salario.</p>
{CTA.replace("@CALC@", "index.html#liq")}
<h2>Qué más se paga al terminar el contrato</h2>
<p>La indemnización se suma a la liquidación ordinaria: cesantías, intereses, prima, vacaciones y salario pendiente. Mira cómo se calcula cada uno en la <a href="como-se-calcula-la-liquidacion.html">guía de liquidación</a>.</p>
<h2>Si el empleador no paga a tiempo</h2>
<p>Al terminar el contrato debe pagarse la liquidación. Si no se hace, puede aplicar indemnización moratoria (CST, art. 65). Antes de firmar un acuerdo o un paz y salvo, valida las cifras con un abogado laboral, un inspector del trabajo o el Ministerio del Trabajo.</p>
<h2>Normas de referencia</h2>
<p>Código Sustantivo del Trabajo, arts. 62, 64 y 65 (modificados por la Ley 789 de 2002). Verifica su vigencia, ya que pueden cambiar.</p>'''

BLOGP = '<p>Guías claras sobre seguridad social, liquidación, horas extra e indemnizaciones en Colombia, con ejemplos numéricos de 2026.</p>' + cards()

def page2(file, title, desc, h1, body, calc, skip=None):
    more = '<h2>Sigue leyendo</h2>' + cards(skip) + '<p><a href="blog.html">← Ver todos los artículos</a> · <a href="index.html#inicio">Volver al inicio</a></p>' if skip else ""
    open(os.path.join(SALIDA, file), "w", encoding="utf-8").write(TPL.replace("@MORE@", more).replace("@BODY@", body).replace("@TITLE@", title).replace("@DESC@", desc).replace("@FILE@", file).replace("@DOM@", DOMINIO).replace("@H1@", h1).replace("@CALC@", calc))
page2("horas-extra.html", "Horas extra y recargos 2026 en Colombia: cómo calcularlos | Calculadora Laboral", "Cómo calcular horas extra, recargo nocturno y dominical en Colombia en 2026 con la jornada de 42 horas, tabla de factores y ejemplo.", "Cómo calcular las horas extra y recargos en Colombia (2026)", HEX, "index.html#hex", "horas-extra.html")
page2("indemnizacion.html", "Indemnización por despido sin justa causa en Colombia 2026 | Calculadora Laboral", "Cómo se calcula la indemnización por despido sin justa causa en contratos indefinidos, fijos y por obra o labor, con ejemplos.", "Indemnización por despido sin justa causa: cómo se calcula", IND, "index.html#liq", "indemnizacion.html")
page2("guia-pila-2026.html", "Guía PILA 2026 para independientes: cómo calcular tu planilla | Calculadora Laboral", "Aprende paso a paso cómo calcular la PILA como independiente en 2026: IBC del 40%, salud, pensión, ARL, fechas de pago y ejemplos.", "Guía PILA 2026 para independientes: cómo calcular tu planilla paso a paso", PILA.replace("@CALC@", "index.html#pila"), "index.html#pila", "guia-pila-2026.html")
page2("como-se-calcula-la-liquidacion.html", "Cómo se calcula la liquidación laboral en Colombia 2026 | Calculadora Laboral", "Cómo calcular cesantías, intereses, prima, vacaciones e indemnización al terminar un contrato en Colombia, con un ejemplo de 2026.", "Cómo se calcula la liquidación laboral en Colombia (2026)", LIQ.replace("@CALC@", "index.html#liq"), "index.html#liq", "como-se-calcula-la-liquidacion.html")
page2("blog.html", "Blog laboral Colombia 2026: guías de PILA, liquidación y horas extra | Calculadora Laboral", "Guías sobre PILA, liquidación, horas extra e indemnización en Colombia con ejemplos numéricos de 2026.", "Blog laboral", BLOGP, "index.html#inicio")


PAGINAS = ["index.html", "blog.html"] + [a[0] for a in ART]
hoy = __import__("datetime").date.today().isoformat()
with open(os.path.join(SALIDA, "sitemap.xml"), "w", encoding="utf-8") as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p_ in PAGINAS:
        fh.write(f"  <url><loc>https://{DOMINIO}/{'' if p_ == 'index.html' else p_}</loc><lastmod>{hoy}</lastmod></url>\n")
    fh.write("</urlset>\n")
print("Listo: se generaron", len(ART) + 2, "páginas y sitemap.xml en", os.path.abspath(SALIDA))
