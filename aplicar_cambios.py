#!/usr/bin/env python3
"""
Aplica todas las correcciones a tu calculadora.

Uso:
    python3 aplicar_cambios.py index.html
Genera: index_corregido.html (el original no se toca).

Si algún fragmento no coincide exactamente, el script se detiene y dice cuál.
"""
import sys

if len(sys.argv) < 2:
    sys.exit("Uso: python3 aplicar_cambios.py tu_archivo.html")

src = sys.argv[1]
out = src.rsplit(".", 1)[0] + "_corregido.html"
h = open(src, encoding="utf-8").read()


def rep(old, new, count=1):
    global h
    n = h.count(old)
    if n != count:
        sys.exit(f"ERROR: se esperaban {count} coincidencias y hay {n} para:\n{old[:120]}")
    h = h.replace(old, new)


# 1. Textos en inglés
rep("× 30 days ÷ 6 = 210", "× 30 días ÷ 6 = 210")
rep("(año de 360 days)", "(año de 360 días)")

# 2. Versión de parámetros (evita valores viejos guardados). Sube v cuando cambies tarifas.
rep("params: {smmlv: 1750905,", "params: {v: 1, smmlv: 1750905,")
rep("S.settings = merge(DEF, j.settings); }",
    "S.settings = merge(DEF, j.settings); "
    "if (!j.settings || !j.settings.params || j.settings.params.v !== DEF.params.v) S.settings.params = clone(DEF.params); }")

# 3. Validación del período (Firefox / Safari de escritorio)
rep('const cap = s => s.charAt(0).toUpperCase() + s.slice(1);',
    'const cap = s => s.charAt(0).toUpperCase() + s.slice(1);\n'
    '  const perOk = v => /^\\d{4}-(0[1-9]|1[0-2])$/.test(v || "");')
rep('const defaultPeriod = () => { const d = today0(); return iso(new Date(d.getFullYear(), d.getMonth() - 1, 1)).slice(0, 7); };',
    'const defaultPeriod = () => { const d = today0(); return iso(new Date(d.getFullYear(), d.getMonth() - 1, 1)).slice(0, 7); };\n'
    '  const perVal = () => { const v = $("pila-periodo").value; return perOk(v) ? v : defaultPeriod(); };')
rep('$("pila-periodo").value || defaultPeriod()', 'perVal()', count=4)
rep('S.settings.paidThrough = per || ""; S.settings.asked = true;',
    'S.settings.paidThrough = perOk(per) ? per : ""; S.settings.asked = true;')
rep('<input type="month" id="pila-periodo">', '<input type="month" id="pila-periodo" placeholder="2026-09">')
rep('<input type="month" id="aj-upto">', '<input type="month" id="aj-upto" placeholder="2026-09">')

# 4. Porcentaje de cotización acotado a 1-100
rep('p.basePct = nv("pila-base") || 40;',
    'p.basePct = Math.min(100, Math.max(1, nv("pila-base") || 40));')

# 5. ARL inválida en Mi sueldo
rep('PCT(ARL[$("sue-arl").value].r)', 'PCT((ARL[$("sue-arl").value] || ARL["1"]).r)')

# 6. Restaurar respaldo con validación
rep('S.records = j.records; S.cobros = Array.isArray(j.cobros) ? j.cobros.filter(c => c && typeof c === "object").map(c => Object.assign({}, c, {id: String(c.id || newId()), valor: Number(c.valor) || 0, paid: !!c.paid})) : [];',
    '''const okD = s => /^\\d{4}-\\d{2}-\\d{2}$/.test(s || "") ? s : "";
        S.records = {};
        Object.keys(j.records).forEach(k => {
          const r = j.records[k];
          if (/^p\\d{6}$/.test(k) && r && /^\\d{4}-\\d{2}$/.test(r.period)) { r.paidOn = okD(r.paidOn); S.records[k] = r; }
        });
        S.cobros = Array.isArray(j.cobros) ? j.cobros.filter(c => c && typeof c === "object").map(c => Object.assign({}, c, {
          id: String(c.id || newId()).replace(/[^\\w-]/g, ""), valor: Number(c.valor) || 0, paid: !!c.paid,
          emision: okD(c.emision), vence: okD(c.vence), paidOn: okD(c.paidOn)})) : [];''')
rep('S.settings = merge(DEF, j.settings); lsSave(); location.reload();',
    'S.settings = merge(DEF, j.settings); '
    'if (!j.settings || !j.settings.params || j.settings.params.v !== DEF.params.v) S.settings.params = clone(DEF.params); '
    'lsSave(); location.reload();')

# 7. Detalles menores
rep('(vencC.length === 1 ? " por reclamar" : " por reclamar")', '" por reclamar"')
rep('/* ============ HISTORIAL ============ */',
    '.blog-card:hover{border-color:var(--accent)!important}\n\n/* ============ HISTORIAL ============ */')
rep('$("pila-periodo").value = nextPila(); $("vac-fin").value = iso(t); $("liq-fin").value = iso(t);',
    '$("pila-periodo").value = nextPila(); $("vac-fin").value = iso(t); $("liq-fin").value = iso(t);\n'
    '    $("liq-aux").checked = true; $("sue-aux").checked = true;')

# 8. Encabezado: favicon, canonical, Open Graph, JSON-LD (se quita meta keywords)
rep('<meta name="keywords" content="calculadora laboral colombia, calcular planilla pila independientes, simulador liquidacion laboral colombia, horas extra colombia 2026">',
    '''<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧮</text></svg>">
<link rel="canonical" href="https://TU-DOMINIO/">
<meta property="og:type" content="website">
<meta property="og:title" content="Calculadora Laboral Colombia 2026">
<meta property="og:description" content="PILA para independientes, liquidación, horas extra y vacaciones.">
<meta property="og:url" content="https://TU-DOMINIO/">''')

faq = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"¿Cómo se calcula el aporte a salud y pensión como independiente?","acceptedAnswer":{"@type":"Answer","text":"Los independientes cotizan sobre un IBC equivalente al 40% de sus ingresos netos mensuales. Sobre ese valor se paga el 12,5% a salud y el 16% a pensión."}},
{"@type":"Question","name":"¿Cuándo vence el pago de la PILA?","acceptedAnswer":{"@type":"Answer","text":"Depende de los dos últimos dígitos de tu cédula o NIT: va del segundo al decimosexto día hábil del mes siguiente al período cotizado, según el Decreto 1990 de 2016."}},
{"@type":"Question","name":"¿Cómo funciona la liquidación por despido sin justa causa?","acceptedAnswer":{"@type":"Answer","text":"En contrato indefinido, 30 días de salario por el primer año y 20 por cada año adicional (si devenga menos de 10 salarios mínimos). En contrato a término fijo, los salarios faltantes para cumplir el plazo pactado."}},
{"@type":"Question","name":"¿Qué aportes debe pagar mi empresa si soy empleado?","acceptedAnswer":{"@type":"Answer","text":"La empresa aporta pensión (12%), ARL y caja (4%), y salud (8,5%), SENA (2%) e ICBF (3%) salvo que sea persona jurídica exonerada. El empleado aporta 4% a salud y 4% a pensión."}}
]}
</script>
</head>'''
rep('</head>', faq)

# 9. Política de privacidad más precisa
rep('No se envían a ningún servidor.',
    'No se envían a ningún servidor propio: el sitio no tiene cuentas ni base de datos.')
rep('lo que permite ofrecer el contenido de forma gratuita.</p>',
    'lo que permite ofrecer el contenido de forma gratuita. Además, las tipografías se cargan desde Google Fonts, por lo que tu navegador se conecta a servidores de Google al visitar el sitio. '
    'Puedes gestionar la publicidad personalizada en adssettings.google.com. Contacto: TU-CORREO@dominio.com.</p>')

open(out, "w", encoding="utf-8").write(h)
print("Listo ->", out)
print("Pendiente: cambia TU-DOMINIO y TU-CORREO@dominio.com, y sube ads.txt, horas-extra.html e indemnizacion.html.")
