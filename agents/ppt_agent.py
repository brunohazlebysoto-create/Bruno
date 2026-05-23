"""PPT Agent — generates a professional PowerPoint presentation using python-pptx."""
import json
import os
import re
import anthropic
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from rich.console import Console

console = Console()

# ── Color palette (medical blue theme) ────────────────────────────────────── #
NAVY    = RGBColor(0x0A, 0x29, 0x5C)   # dark navy
BLUE    = RGBColor(0x1A, 0x6B, 0xC4)   # primary blue
CYAN    = RGBColor(0x00, 0xB4, 0xD8)   # accent cyan
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT   = RGBColor(0xF0, 0xF4, 0xFF)   # slide background tint
GRAY    = RGBColor(0x44, 0x44, 0x55)
GREEN   = RGBColor(0x22, 0x8B, 0x22)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

SYSTEM = """Eres un cirujano pediatra docente experto en presentaciones académicas de cirugía infantil.
Devuelve SOLO JSON válido con el contenido de las diapositivas. Sin texto extra."""

PPT_CONTENT_PROMPT = """Crea el contenido para una clase académica de CIRUGÍA INFANTIL sobre: "{topic}"

Usa este meta-análisis como base:
{meta_summary}

Devuelve SOLO un JSON con esta estructura exacta (mínimo 18 slides):
{{
  "titulo_presentacion": "<título>",
  "subtitulo": "<subtítulo con 'Cirugía Infantil — Evidencia Actualizada'>",
  "autor": "Revisión Sistemática Basada en Evidencia",
  "fecha": "{fecha}",
  "slides": [
    {{
      "tipo": "titulo",
      "titulo": "<título completo>",
      "subtitulo": "Cirugía Infantil · Revisión Sistemática Basada en Evidencia",
      "badge": "<badge, ej: Meta-análisis {fecha}>"
    }},
    {{
      "tipo": "objetivos",
      "titulo": "Objetivos de Aprendizaje",
      "items": [
        "Conocer la epidemiología y fisiopatología en el paciente pediátrico",
        "Identificar las manifestaciones clínicas según grupo etario",
        "Aplicar los criterios diagnósticos y estudios de imagen",
        "Seleccionar la técnica quirúrgica basada en la evidencia",
        "Reconocer y manejar las complicaciones quirúrgicas"
      ]
    }},
    {{
      "tipo": "contenido",
      "titulo": "Epidemiología en Pediatría",
      "subtitulo": "Incidencia · Grupos etarios · Factores de riesgo",
      "puntos": ["<dato epidemiológico 1>", "<dato epidemiológico 2>", "<dato 3>", "<dato 4>"]
    }},
    {{
      "tipo": "contenido",
      "titulo": "Embriología y Fisiopatología",
      "subtitulo": "Bases anatómicas y mecanismo fisiopatológico",
      "puntos": ["<mecanismo 1>", "<mecanismo 2>", "<mecanismo 3>", "<mecanismo 4>"]
    }},
    {{
      "tipo": "tabla",
      "titulo": "Manifestaciones Clínicas por Grupo Etario",
      "headers": ["Grupo etario", "Síntoma principal", "Signo clave", "Presentación"],
      "rows": [
        ["Neonato", "<síntoma>", "<signo>", "<presentación>"],
        ["Lactante", "<síntoma>", "<signo>", "<presentación>"],
        ["Preescolar", "<síntoma>", "<signo>", "<presentación>"],
        ["Escolar", "<síntoma>", "<signo>", "<presentación>"]
      ]
    }},
    {{
      "tipo": "contenido",
      "titulo": "Diagnóstico: Clínica y Laboratorio",
      "subtitulo": "Evaluación inicial del paciente pediátrico",
      "puntos": ["<criterio diagnóstico 1>", "<criterio 2>", "<laboratorio>", "<score>"]
    }},
    {{
      "tipo": "contenido",
      "titulo": "Diagnóstico: Imagen",
      "subtitulo": "Técnica de elección y hallazgos característicos",
      "puntos": ["<técnica de imagen preferida>", "<hallazgo característico>", "<criterio imagen>", "<limitación>"]
    }},
    {{
      "tipo": "tabla",
      "titulo": "Diagnóstico Diferencial",
      "headers": ["Diagnóstico", "Diferencia clave", "Estudio confirmatorio"],
      "rows": [["<dx1>", "<diferencia>", "<estudio>"], ["<dx2>", "<diferencia>", "<estudio>"], ["<dx3>", "<diferencia>", "<estudio>"]]
    }},
    {{
      "tipo": "contenido",
      "titulo": "Preparación Preoperatoria",
      "subtitulo": "Estabilización y corrección metabólica",
      "puntos": ["<resucitación>", "<metas metabólicas>", "<ayuno pediátrico 6-4-2-1>", "<profilaxis antibiótica dosis>"]
    }},
    {{
      "tipo": "contenido",
      "titulo": "Consideraciones Anestésicas Pediátricas",
      "subtitulo": "Particularidades del paciente quirúrgico pediátrico",
      "puntos": ["<tipo anestesia>", "<manejo vía aérea>", "<bloqueo regional>", "<monitorización temperatura>"]
    }},
    {{
      "tipo": "contenido",
      "titulo": "Técnica Quirúrgica — Abordaje Preferido",
      "subtitulo": "Paso a paso de la técnica basada en evidencia",
      "puntos": ["<paso 1>", "<paso 2>", "<paso 3>", "<punto crítico>"]
    }},
    {{
      "tipo": "contenido",
      "titulo": "Técnica Quirúrgica — Variantes y Alternativas",
      "subtitulo": "Indicaciones para técnica alternativa",
      "puntos": ["<indicación alternativa>", "<técnica alternativa>", "<conversión>", "<decisión intraoperatoria>"]
    }},
    {{
      "tipo": "contenido",
      "titulo": "Cuidados Postoperatorios",
      "subtitulo": "Manejo en sala y criterios de alta",
      "puntos": ["<monitorización>", "<analgesia multimodal dosis mg/kg>", "<realimentación>", "<criterios de alta>"]
    }},
    {{
      "tipo": "tabla",
      "titulo": "Complicaciones Quirúrgicas",
      "headers": ["Complicación", "Incidencia", "Manejo"],
      "rows": [
        ["<complicación 1>", "<incidencia>", "<manejo>"],
        ["<complicación 2>", "<incidencia>", "<manejo>"],
        ["<complicación 3>", "<incidencia>", "<manejo>"],
        ["<complicación 4>", "<incidencia>", "<manejo>"]
      ]
    }},
    {{
      "tipo": "evidencia",
      "titulo": "Síntesis de la Evidencia",
      "nivel_global": "<nivel Oxford CEBM>",
      "grado": "<grado A-D>",
      "consenso": "<alto/moderado/bajo>",
      "puntos": ["<hallazgo evidencia 1>", "<hallazgo 2>", "<hallazgo 3>", "<recomendación técnica>"]
    }},
    {{
      "tipo": "tabla",
      "titulo": "Principales Estudios — Tabla de Evidencia",
      "headers": ["Referencia", "Tipo", "N", "Resultado clave", "Nivel evidencia"],
      "rows": [
        ["<Autor et al., Año>", "<tipo>", "<n>", "<resultado>", "<nivel>"],
        ["<Autor et al., Año>", "<tipo>", "<n>", "<resultado>", "<nivel>"],
        ["<Autor et al., Año>", "<tipo>", "<n>", "<resultado>", "<nivel>"]
      ]
    }},
    {{
      "tipo": "conclusiones",
      "titulo": "Conclusiones y Recomendaciones",
      "items": [
        "<conclusión técnica quirúrgica>",
        "<conclusión diagnóstica>",
        "<conclusión perioperatoria>",
        "<área de controversia>",
        "<perspectivas futuras>"
      ]
    }},
    {{
      "tipo": "preguntas",
      "titulo": "Preguntas y Discusión"
    }}
  ]
}}

Mínimo 18 slides. Todos los contenidos deben ser específicos de CIRUGÍA INFANTIL
con datos numéricos reales (incidencias, dosis mg/kg, tasas de complicaciones).
Fecha: {fecha}.
"""


# ── Helper drawing functions ────────────────────────────────────────────────── #

def _add_rect(slide, left, top, width, height, fill_color, transparency=0):
    shape = slide.shapes.add_shape(1, left, top, width, height)  # MSO_SHAPE_TYPE.RECTANGLE
    shape.line.fill.background()
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = fill_color
    if transparency:
        fill.fore_color.theme_color = None
    return shape


def _add_text_box(slide, text, left, top, width, height,
                  font_size=18, bold=False, color=WHITE, align=PP_ALIGN.LEFT,
                  wrap=True):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return txBox


def _set_slide_bg(slide, color: RGBColor):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


# ── Slide builders ──────────────────────────────────────────────────────────── #

def _build_title_slide(prs: Presentation, data: dict):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    _set_slide_bg(slide, NAVY)

    # Top accent bar
    _add_rect(slide, 0, 0, SLIDE_W, Inches(0.12), CYAN)

    # Bottom bar
    _add_rect(slide, 0, Inches(6.8), SLIDE_W, Inches(0.7), BLUE)

    # Badge
    badge = data.get("badge", "")
    if badge:
        _add_rect(slide, Inches(0.5), Inches(1.0), Inches(3.5), Inches(0.45), CYAN)
        _add_text_box(slide, badge.upper(), Inches(0.55), Inches(1.0),
                      Inches(3.4), Inches(0.45), font_size=11, bold=True,
                      color=NAVY, align=PP_ALIGN.CENTER)

    # Main title
    _add_text_box(slide, data.get("titulo", ""), Inches(0.5), Inches(1.7),
                  Inches(12.3), Inches(2.0), font_size=40, bold=True,
                  color=WHITE, align=PP_ALIGN.LEFT)

    # Subtitle
    _add_text_box(slide, data.get("subtitulo", ""), Inches(0.5), Inches(3.8),
                  Inches(10), Inches(0.8), font_size=22, bold=False,
                  color=CYAN, align=PP_ALIGN.LEFT)

    # Author / date
    _add_text_box(slide, data.get("autor", ""), Inches(0.5), Inches(4.8),
                  Inches(8), Inches(0.5), font_size=16, color=LIGHT)
    _add_text_box(slide, data.get("fecha", ""), Inches(0.5), Inches(5.3),
                  Inches(4), Inches(0.4), font_size=14, color=RGBColor(0xAA, 0xCC, 0xFF))


def _build_content_slide(prs: Presentation, data: dict):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, LIGHT)

    # Header bar
    _add_rect(slide, 0, 0, SLIDE_W, Inches(1.2), NAVY)
    _add_rect(slide, 0, Inches(1.2), Inches(0.08), Inches(6.3), CYAN)

    title = data.get("titulo", "")
    _add_text_box(slide, title, Inches(0.3), Inches(0.15),
                  Inches(12.5), Inches(0.9), font_size=28, bold=True,
                  color=WHITE, align=PP_ALIGN.LEFT)

    subtitle = data.get("subtitulo", "")
    if subtitle:
        _add_text_box(slide, subtitle, Inches(0.3), Inches(1.0),
                      Inches(12), Inches(0.35), font_size=15,
                      color=RGBColor(0xAA, 0xCC, 0xFF), align=PP_ALIGN.LEFT)

    puntos = data.get("puntos", [])
    top = Inches(1.5)
    for punto in puntos[:7]:
        # bullet dot
        _add_rect(slide, Inches(0.35), top + Inches(0.1), Inches(0.12), Inches(0.12), CYAN)
        _add_text_box(slide, punto, Inches(0.6), top,
                      Inches(12.3), Inches(0.6), font_size=18,
                      color=GRAY, align=PP_ALIGN.LEFT)
        top += Inches(0.72)

    # Slide number bottom-right
    _add_text_box(slide, "●", Inches(12.5), Inches(7.1),
                  Inches(0.5), Inches(0.3), font_size=10, color=NAVY)


def _build_objectives_slide(prs: Presentation, data: dict):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, WHITE)
    _add_rect(slide, 0, 0, SLIDE_W, Inches(1.4), BLUE)
    _add_rect(slide, 0, Inches(1.4), SLIDE_W, Inches(0.06), CYAN)

    _add_text_box(slide, data.get("titulo", "Objetivos"), Inches(0.4), Inches(0.25),
                  Inches(12), Inches(1.0), font_size=32, bold=True,
                  color=WHITE, align=PP_ALIGN.LEFT)

    items = data.get("items", [])
    icons = ["🎯", "📋", "🔬", "💡", "📊", "🏥"]
    top = Inches(1.7)
    for i, item in enumerate(items[:6]):
        icon = icons[i % len(icons)]
        _add_rect(slide, Inches(0.4), top, Inches(11.5), Inches(0.75),
                  RGBColor(0xE8, 0xF0, 0xFF))
        _add_text_box(slide, f"  {icon}  {item}", Inches(0.5), top + Inches(0.08),
                      Inches(11), Inches(0.62), font_size=18,
                      color=NAVY, align=PP_ALIGN.LEFT)
        top += Inches(0.88)


def _build_tabla_slide(prs: Presentation, data: dict):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, LIGHT)
    _add_rect(slide, 0, 0, SLIDE_W, Inches(1.2), NAVY)

    _add_text_box(slide, data.get("titulo", "Tabla"), Inches(0.3), Inches(0.2),
                  Inches(12.5), Inches(0.85), font_size=26, bold=True,
                  color=WHITE, align=PP_ALIGN.LEFT)

    headers = data.get("headers", [])
    rows = data.get("rows", [])
    if not headers:
        return

    cols = len(headers)
    col_w = Inches(12.8) / cols
    top = Inches(1.3)

    # Header row
    for ci, h in enumerate(headers):
        _add_rect(slide, Inches(0.25) + col_w * ci, top, col_w - Inches(0.05),
                  Inches(0.55), BLUE)
        _add_text_box(slide, h, Inches(0.3) + col_w * ci, top,
                      col_w, Inches(0.55), font_size=14, bold=True,
                      color=WHITE, align=PP_ALIGN.CENTER)

    top += Inches(0.6)
    for ri, row in enumerate(rows[:8]):
        bg = RGBColor(0xE8, 0xF0, 0xFF) if ri % 2 == 0 else WHITE
        for ci, cell in enumerate(row[:cols]):
            _add_rect(slide, Inches(0.25) + col_w * ci, top, col_w - Inches(0.05),
                      Inches(0.52), bg)
            _add_text_box(slide, str(cell), Inches(0.3) + col_w * ci, top,
                          col_w, Inches(0.52), font_size=13,
                          color=GRAY, align=PP_ALIGN.CENTER)
        top += Inches(0.55)


def _build_evidence_slide(prs: Presentation, data: dict):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, NAVY)
    _add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), CYAN)

    _add_text_box(slide, data.get("titulo", "Síntesis de Evidencia"),
                  Inches(0.4), Inches(0.2), Inches(12), Inches(1.0),
                  font_size=30, bold=True, color=WHITE)

    # Badges
    nivel = data.get("nivel_global", "")
    grado = data.get("grado", "")
    consenso = data.get("consenso", "")

    badges = [
        (f"Nivel: {nivel}", CYAN, NAVY),
        (f"Grado: {grado}", GREEN, WHITE),
        (f"Consenso: {consenso}", BLUE, WHITE),
    ]
    bx = Inches(0.4)
    for label, bg, fg in badges:
        _add_rect(slide, bx, Inches(1.3), Inches(2.8), Inches(0.6), bg)
        _add_text_box(slide, label, bx, Inches(1.3), Inches(2.8), Inches(0.6),
                      font_size=16, bold=True, color=fg, align=PP_ALIGN.CENTER)
        bx += Inches(3.1)

    puntos = data.get("puntos", [])
    top = Inches(2.2)
    for p in puntos[:5]:
        _add_rect(slide, Inches(0.4), top, Inches(0.5), Inches(0.5), CYAN)
        _add_text_box(slide, "✓", Inches(0.4), top, Inches(0.5), Inches(0.5),
                      font_size=18, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
        _add_text_box(slide, p, Inches(1.0), top, Inches(11.8), Inches(0.6),
                      font_size=17, color=LIGHT)
        top += Inches(0.82)


def _build_conclusions_slide(prs: Presentation, data: dict):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, WHITE)
    _add_rect(slide, 0, 0, SLIDE_W, Inches(1.3), NAVY)
    _add_rect(slide, 0, Inches(1.3), SLIDE_W, Inches(0.07), CYAN)

    _add_text_box(slide, data.get("titulo", "Conclusiones"),
                  Inches(0.4), Inches(0.2), Inches(12), Inches(1.0),
                  font_size=30, bold=True, color=WHITE)

    items = data.get("items", [])
    top = Inches(1.55)
    for i, item in enumerate(items[:6], 1):
        _add_rect(slide, Inches(0.4), top, Inches(0.55), Inches(0.55), NAVY)
        _add_text_box(slide, str(i), Inches(0.4), top, Inches(0.55), Inches(0.55),
                      font_size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        _add_text_box(slide, item, Inches(1.1), top, Inches(11.7), Inches(0.7),
                      font_size=17, color=GRAY)
        top += Inches(0.85)


def _build_questions_slide(prs: Presentation, data: dict):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, BLUE)
    _add_rect(slide, 0, 0, SLIDE_W, Inches(0.1), CYAN)
    _add_rect(slide, 0, Inches(7.4), SLIDE_W, Inches(0.1), CYAN)

    _add_text_box(slide, "❓", Inches(5.5), Inches(1.5), Inches(2), Inches(2),
                  font_size=80, color=WHITE, align=PP_ALIGN.CENTER)
    _add_text_box(slide, data.get("titulo", "Preguntas y Discusión"),
                  Inches(1), Inches(3.8), Inches(11.3), Inches(1.2),
                  font_size=36, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    _add_text_box(slide, "Basado en evidencia científica actualizada",
                  Inches(2), Inches(5.2), Inches(9.3), Inches(0.7),
                  font_size=18, color=LIGHT, align=PP_ALIGN.CENTER)


BUILDERS = {
    "titulo": _build_title_slide,
    "objetivos": _build_objectives_slide,
    "contenido": _build_content_slide,
    "tabla": _build_tabla_slide,
    "evidencia": _build_evidence_slide,
    "conclusiones": _build_conclusions_slide,
    "preguntas": _build_questions_slide,
}


class PPTAgent:
    """Generates a professional PowerPoint medical lecture."""

    name = "Agente Presentador"
    description = (
        "Docente médico experto en presentaciones académicas. "
        "Genera diapositivas profesionales con diseño médico moderno."
    )

    def __init__(self, api_key: str = ""):
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        )

    def _get_slide_content(self, topic: str, meta: dict) -> dict:
        import datetime
        meta_summary = json.dumps({
            "conclusion": meta.get("conclusion_sintetica", ""),
            "hallazgos": meta.get("hallazgos_principales", [])[:5],
            "nivel_evidencia": meta.get("nivel_evidencia_global", ""),
            "grado": meta.get("grado_recomendacion_global", ""),
            "consenso": meta.get("areas_consenso", [])[:3],
            "controversia": meta.get("areas_controversia", [])[:2],
            "implicaciones": meta.get("implicaciones_clinicas", [])[:4],
        }, ensure_ascii=False)

        fecha = datetime.date.today().strftime("%B %Y")
        prompt = PPT_CONTENT_PROMPT.format(
            topic=topic,
            meta_summary=meta_summary,
            fecha=fecha,
        )
        msg = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=6000,
            system=SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)

    def run(self, topic: str, meta: dict, output_path: str) -> str:
        console.print(
            f"\n[bold cyan]🎨 {self.name}[/bold cyan] — creando presentación PowerPoint\n"
        )
        with console.status("  Generando contenido de diapositivas..."):
            content = self._get_slide_content(topic, meta)

        slides_data = content.get("slides", [])
        console.print(f"  → {len(slides_data)} diapositivas planificadas")

        # Build presentation
        prs = Presentation()
        prs.slide_width  = SLIDE_W
        prs.slide_height = SLIDE_H

        for slide_data in slides_data:
            tipo = slide_data.get("tipo", "contenido")
            # Map titulo slide data fields
            if tipo == "titulo":
                slide_data.setdefault("titulo", content.get("titulo_presentacion", topic))
                slide_data.setdefault("subtitulo", content.get("subtitulo", ""))
                slide_data.setdefault("autor", content.get("autor", ""))
                slide_data.setdefault("fecha", content.get("fecha", ""))

            builder = BUILDERS.get(tipo, _build_content_slide)
            try:
                builder(prs, slide_data)
            except Exception as e:
                console.print(f"  [yellow]! Slide '{tipo}' error:[/yellow] {e}")
                _build_content_slide(prs, {"titulo": slide_data.get("titulo", tipo),
                                            "puntos": ["Error al generar esta diapositiva"]})

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        prs.save(output_path)
        console.print(f"  [bold]✓ PowerPoint guardado:[/bold] {output_path}\n")
        return output_path
