"""Configuración personalizable de la interfaz Streamlit.

Los alumnos pueden modificar este fichero para adaptar la app a su prueba.
Streamlit recarga automáticamente al detectar cambios en disco.
"""

# ---------------------------------------------------------------------------
# Identidad del agente
# ---------------------------------------------------------------------------
AGENT_NAME = "Verde Vida"
AGENT_ICON = "🌿"
AGENT_SUBTITLE = "Asesora del vivero Verde Vida — Curso LLMOps"

# ---------------------------------------------------------------------------
# Página
# ---------------------------------------------------------------------------
PAGE_TITLE = "Verde Vida — Vivero"
PAGE_ICON = "🌿"
PAGE_LAYOUT = "centered"  # "centered" | "wide"

# ---------------------------------------------------------------------------
# Metadatos de tracing (aparecen en Langfuse)
# ---------------------------------------------------------------------------
TRACING_USER_ID = "streamlit-student"
TRACING_SOURCE = "streamlit_app"

# ---------------------------------------------------------------------------
# Preguntas de ejemplo (sidebar)
# ---------------------------------------------------------------------------
EXAMPLES: list[str] = [
    "¿Qué plantas de interior tenéis por menos de 20 €?",
    "¿Cuál es la política de devoluciones?",
    "Recomiéndame un árbol frutal para el jardín",
    "¿Hacéis envíos internacionales?",
    "¿Qué plantas aromáticas tenéis disponibles?",
    "¿Cuánto cuesta el Limonero Luna?",
]

# ---------------------------------------------------------------------------
# Entornos de prompt (label de Langfuse)
# Los alumnos pueden añadir entornos custom si crean labels adicionales.
# Formato: { "Nombre visible en UI": "label_en_langfuse" }
#
# Labels habituales en Langfuse:
#   "production"  — prompt activo en producción
#   "staging"     — candidato bajo evaluación
#   "development" — experimentación libre de los alumnos
#   "latest"      — label especial de Langfuse, siempre apunta a la última
#                    versión creada (NO usar como entorno, solo para debug)
# ---------------------------------------------------------------------------
ENVIRONMENTS: dict[str, str] = {
    "🟢 Production": "production",
    "🟡 Staging": "staging",
    "🔵 Development": "development",
}
