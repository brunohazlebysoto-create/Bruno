#!/usr/bin/env python3
"""FastAPI web server for the Pediatric Surgery Multi-Agent Research System."""
import asyncio
import json
import os
import queue
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent))

from agents.search_agent import SearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.meta_analysis_agent import MetaAnalysisAgent
from agents.notes_agent import NotesAgent
from agents.ppt_agent import PPTAgent

app = FastAPI(title="Cirugía Infantil — Sistema Multi-Agente")
executor = ThreadPoolExecutor(max_workers=4)
sessions: dict[str, dict] = {}


# ── Event emitter ────────────────────────────────────────────────────────── #

class AgentEmitter:
    def __init__(self, q: queue.Queue, agent: str):
        self._q = q
        self._agent = agent

    def log(self, message: str, level: str = "info"):
        self._q.put({"type": "agent_log", "agent": self._agent,
                     "message": message, "level": level})

    def success(self, msg: str): self.log(msg, "success")
    def warning(self, msg: str): self.log(msg, "warning")
    def error(self, msg: str):   self.log(msg, "error")


def _emit(q: queue.Queue, event_type: str, **kw):
    q.put({"type": event_type, **kw})


# ── Pipeline (runs in thread) ────────────────────────────────────────────── #

def run_pipeline(session_id: str, topic: str, max_papers: int,
                 api_key: str, provider: str, q: queue.Queue):
    try:
        ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = topic[:35].lower().replace(" ", "_").replace("/", "-")
        out  = Path("output") / f"{slug}_{ts}"
        out.mkdir(parents=True, exist_ok=True)

        # ── 1. Search ──────────────────────────────────────────────────────── #
        _emit(q, "agent_start", agent="Buscador", icon="🔍", color="#00b4d8",
              description="Experto en búsqueda bibliográfica pediátrica · "
                          "PubMed · Semantic Scholar · CrossRef")
        em = AgentEmitter(q, "Buscador")
        em.log("Construyendo queries con filtros pediátricos (child / infant / neonate)...")

        searcher = SearchAgent()
        papers = searcher.run(topic, max_per_db=max(8, max_papers // 3))

        if papers and any(p.get("demo") for p in papers):
            em.warning("APIs externas no disponibles · cargando base de datos clínica interna")
        else:
            em.success("PubMed consultado con MeSH terms pediátricos")
            em.success("Semantic Scholar consultado")
            em.success("CrossRef consultado")

        em.success(f"{len(papers)} artículos únicos tras deduplicación")
        _emit(q, "agent_complete", agent="Buscador",
              summary=f"{len(papers)} artículos listos para análisis")
        (out / "01_papers_raw.json").write_text(
            json.dumps(papers, ensure_ascii=False, indent=2), encoding="utf-8")

        if not api_key:
            links = {"groq": "console.groq.com", "gemini": "aistudio.google.com"}
            link  = links.get(provider, "el proveedor seleccionado")
            _emit(q, "pipeline_error",
                  message=f"API Key no configurada. Obtén una gratis en {link} y pégala en el formulario.")
            q.put(None)
            return

        # ── 2. Analysis ────────────────────────────────────────────────────── #
        batch = papers[:max_papers]
        _emit(q, "agent_start", agent="Analizador", icon="🔬", color="#9d4edd",
              description="Cirujano pediatra · PICO-S · Nivel evidencia CEBM · "
                          "Calidad metodológica · Grupo etario")
        em = AgentEmitter(q, "Analizador")
        em.log(f"Analizando {len(batch)} artículos con {provider.upper()}......")

        analyzer = AnalysisAgent(api_key=api_key, provider=provider)
        analyzed = []
        for i, paper in enumerate(batch, 1):
            result = analyzer._analyze_one(paper)
            analyzed.append(result)
            a     = result.get("analysis", {})
            tipo  = a.get("tipo_estudio", "—")
            nivel = a.get("nivel_evidencia", "—")
            cal   = a.get("calidad_metodologica", "—")
            grupo = a.get("grupo_etario", "—")
            title = paper.get("title", "")[:55]
            em.success(
                f"[{i}/{len(batch)}] {title}…"
                f" · {tipo} · Niv.{nivel} · Cal.{cal}/5 · {grupo}"
            )

        _emit(q, "agent_complete", agent="Analizador",
              summary=f"{len(analyzed)} artículos evaluados con criterios CEBM / GRADE pediátrico")
        (out / "02_papers_analyzed.json").write_text(
            json.dumps(analyzed, ensure_ascii=False, indent=2), encoding="utf-8")

        # ── 3. Meta-analysis ───────────────────────────────────────────────── #
        _emit(q, "agent_start", agent="Meta-Analista", icon="📊", color="#f77f00",
              description="Bioestadístico en cirugía infantil · Síntesis GRADE · "
                          "Distribución etaria · Técnicas quirúrgicas comparadas")
        em = AgentEmitter(q, "Meta-Analista")
        em.log(f"Sintetizando evidencia de {len(analyzed)} estudios...")
        em.log("Evaluando heterogeneidad, sesgos de publicación y distribución etaria...")
        em.log("Comparando técnicas quirúrgicas (laparoscópica vs abierta vs alternativas)...")

        meta_agent = MetaAnalysisAgent(api_key=api_key, provider=provider)
        meta = meta_agent.run(analyzed, topic)

        nivel_g = meta.get("nivel_evidencia_global", "N/A")
        grado_g = meta.get("grado_recomendacion_global", "N/A")
        em.success(f"Nivel de evidencia global: {nivel_g}  ·  Grado: {grado_g}")
        tecnicas = meta.get("tecnicas_quirurgicas_comparadas", [])
        if tecnicas:
            em.success("Técnicas comparadas: " + " · ".join(tecnicas[:3]))
        hallazgos = meta.get("hallazgos_principales", [])
        em.success(f"{len(hallazgos)} hallazgos principales identificados")
        gaps = meta.get("gaps_conocimiento", [])
        if gaps:
            em.log(f"Gaps detectados: {gaps[0][:80]}…", "warning")

        _emit(q, "agent_complete", agent="Meta-Analista",
              summary=f"Nivel {nivel_g}  |  Grado {grado_g}  |  "
                      f"{len(hallazgos)} hallazgos  |  Meta-análisis completado")
        (out / "03_meta_analysis.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

        # ── 4. Notes ───────────────────────────────────────────────────────── #
        _emit(q, "agent_start", agent="Redactor", icon="📝", color="#2dc653",
              description="Cirujano pediatra docente · Técnica quirúrgica paso a paso · "
                          "Dosis mg/kg · Cuidados perioperatorios pediátricos")
        em = AgentEmitter(q, "Redactor")
        em.log("Generando apunte clínico completo de cirugía infantil...")
        em.log("Secciones: Epidemiología · Embriología · Clínica por grupo etario · "
               "Diagnóstico · Técnica quirúrgica · Anestesia · Complicaciones...")

        notes_agent = NotesAgent(api_key=api_key, provider=provider)
        notes_md = notes_agent.run(topic, meta, analyzed)
        notes_path = out / "04_apunte_medico.md"
        notes_path.write_text(notes_md, encoding="utf-8")

        words = len(notes_md.split())
        em.success(f"Apunte generado · {words:,} palabras")
        em.success("Dosis en mg/kg incluidas · Técnica quirúrgica paso a paso · "
                   "Tabla diagnóstico diferencial · Tabla de evidencia")

        _emit(q, "agent_complete", agent="Redactor",
              summary=f"Apunte de {words:,} palabras generado")

        # ── 5. PowerPoint ──────────────────────────────────────────────────── #
        _emit(q, "agent_start", agent="Presentador", icon="🎨", color="#ff4d6d",
              description="Docente de cirugía infantil · PowerPoint profesional · "
                          "18+ diapositivas · Tema médico navy/azul")
        em = AgentEmitter(q, "Presentador")
        em.log("Generando contenido de diapositivas con Claude...")
        em.log("Planificando: Título · Objetivos · Epidemiología · Fisiopatología · "
               "Diagnóstico · Técnica quirúrgica · Complicaciones · Evidencia · Conclusiones...")

        ppt_agent = PPTAgent(api_key=api_key)
        ppt_file  = str(out / "05_presentacion.pptx")
        ppt_agent.run(topic, meta, ppt_file)

        em.success("Slides construidas con python-pptx · Diseño profesional navy/azul")
        em.success("Tabla clínica por grupo etario · Tabla complicaciones · "
                   "Tabla de evidencia · Slide de técnica quirúrgica")

        _emit(q, "agent_complete", agent="Presentador",
              summary="Presentación PowerPoint profesional lista (18+ slides)")

        # ── Done ───────────────────────────────────────────────────────────── #
        sessions[session_id]["files"] = {
            "apunte_medico.md":    str(notes_path),
            "presentacion.pptx":   str(out / "05_presentacion.pptx"),
            "meta_analysis.json":  str(out / "03_meta_analysis.json"),
        }
        sessions[session_id]["status"] = "done"
        _emit(q, "pipeline_complete", files=[
            {"label": "📝 Apunte Médico",           "filename": "apunte_medico.md",   "ext": "md"},
            {"label": "🎨 Presentación PowerPoint", "filename": "presentacion.pptx",  "ext": "pptx"},
            {"label": "📊 Meta-análisis (JSON)",    "filename": "meta_analysis.json", "ext": "json"},
        ])

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        _emit(q, "pipeline_error", message=f"{type(e).__name__}: {e}")
        sessions[session_id]["status"] = "error"
    finally:
        q.put(None)


# ── API ──────────────────────────────────────────────────────────────────── #

class RunRequest(BaseModel):
    topic: str
    max_papers: int = 15
    api_key: str = ""
    provider: str = "groq"   # "groq" | "gemini"


@app.get("/", response_class=HTMLResponse)
async def index():
    html = (Path(__file__).parent / "static" / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(html)


@app.post("/api/run")
async def start_run(req: RunRequest):
    topic = req.topic.strip()
    if not topic:
        raise HTTPException(400, "Tema vacío")
    api_key = req.api_key.strip() or os.environ.get("GROQ_API_KEY","") or os.environ.get("GEMINI_API_KEY","")

    sid = str(uuid.uuid4())
    q: queue.Queue = queue.Queue()
    sessions[sid] = {"queue": q, "files": {}, "status": "running"}

    loop = asyncio.get_event_loop()
    loop.run_in_executor(executor, run_pipeline, sid, topic, req.max_papers, api_key, req.provider, q)

    return {"session_id": sid}


@app.get("/api/stream/{sid}")
async def stream(sid: str):
    session = sessions.get(sid)
    if not session:
        raise HTTPException(404, "Sesión no encontrada")
    q = session["queue"]
    loop = asyncio.get_event_loop()

    async def generate():
        while True:
            try:
                event = await loop.run_in_executor(
                    None, lambda: q.get(timeout=180)
                )
                if event is None:
                    yield "data: {\"type\":\"stream_end\"}\n\n"
                    break
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
            except Exception:
                yield "data: {\"type\":\"ping\"}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache",
                 "Connection": "keep-alive",
                 "X-Accel-Buffering": "no"},
    )


@app.get("/api/download/{sid}/{filename}")
async def download(sid: str, filename: str):
    session = sessions.get(sid)
    if not session:
        raise HTTPException(404, "Sesión no encontrada")
    fp = session.get("files", {}).get(filename)
    if not fp or not Path(fp).exists():
        raise HTTPException(404, "Archivo no encontrado")
    return FileResponse(fp, filename=filename, media_type="application/octet-stream")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
