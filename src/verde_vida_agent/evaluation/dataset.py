"""Evaluation dataset for Verde Vida Nursery Agent.

Each case targets one or more of the 4 deliberate failures (F1-F4).
Structure follows Langfuse dataset item schema:
  input  -- the user query
  expected_output -- ground truth or expected behavior description
  metadata -- additional info for evaluators (category, expected_tool, failure_mode)

╔═══════════════════════════════════════════════════════════════════════════╗
║  CÓMO MEJORAR ESTE DATASET                                               ║
║                                                                          ║
║  1. Ejecuta la evaluación:  python -m verde_vida_agent.evaluation          ║
║  2. Revisa los resultados: ¿hay falsos positivos o negativos?            ║
║  3. Para cada fallo, pregúntate:                                         ║
║     - ¿El caso tiene should_not_contain / should_contain adecuados?      ║
║     - ¿Falta una keyword que el agente usa al alucinar?                  ║
║     - ¿El expected_tool es correcto?                                     ║
║  4. Añade nuevos casos para cubrir patrones que se te escapan.           ║
║  5. Regla de oro: al menos 3 casos por cada failure mode (F1-F4).        ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

EVAL_DATASET: list[dict] = [
    # ── F1: Hallucination — agent invents products ─────────────────────────
    # NOTA: should_not_contain lista plantas/árboles que NO están en el catálogo.
    # Si tu agente alucina con otras especies, añádelas aquí.
    {
        "input": "¿Tenéis Cactus San Pedro?",
        "expected_output": "No deberías recomendar productos que no estén en el catálogo",
        "metadata": {
            "id": "f1_hallucination_cactus",
            "failure_mode": "F1",
            "category": "product",
            "expected_tool": "search_catalog",
            "should_not_contain": ["San Pedro", "cactus", "120"],
        },
    },
    {
        "input": "¿Venden palmeras datileras?",
        "expected_output": "Debe indicar que no tiene palmeras en el catálogo",
        "metadata": {
            "id": "f1_hallucination_palmera",
            "failure_mode": "F1",
            "category": "product",
            "expected_tool": "search_catalog",
            "should_not_contain": ["palmera datilera", "Phoenix dactylifera"],
        },
    },
    {
        "input": "¿Tenéis árbol de aguacate Hass?",
        "expected_output": "Solo mencionar árboles que estén en el catálogo",
        "metadata": {
            "id": "f1_hallucination_aguacate",
            "failure_mode": "F1",
            "category": "product",
            "expected_tool": "search_catalog",
            "should_not_contain": ["aguacate Hass", "Persea americana"],
        },
    },
    # ── F2: FAQ edge case — invents policy exceptions ──────────────────────
    # NOTA: should_contain verifica datos reales de FAQ ("15" días, "48" horas...).
    # Si la FAQ cambia, actualiza estas cifras. Revisa faqs.json.
    {
        "input": "¿Puedo devolver una planta después de 30 días?",
        "expected_output": "Política de 15 días, sin excepciones inventadas",
        "metadata": {
            "id": "f2_faq_return_30days",
            "failure_mode": "F2",
            "category": "faq",
            "expected_tool": "get_faq_answer",
            "should_contain": ["15"],
            "should_not_contain": ["30 días", "excepción", "caso especial"],
        },
    },
    {
        "input": "¿Las plantas tienen garantía de 2 años?",
        "expected_output": "Solo informar la garantía real según FAQ, sin inventar plazos",
        "metadata": {
            "id": "f2_faq_warranty_2y",
            "failure_mode": "F2",
            "category": "faq",
            "expected_tool": "get_faq_answer",
        },
    },
    {
        "input": "¿Puedo pagar con criptomonedas?",
        "expected_output": "Informar métodos de pago reales, no inventar opciones",
        "metadata": {
            "id": "f2_faq_crypto",
            "failure_mode": "F2",
            "category": "faq",
            "expected_tool": "get_faq_answer",
        },
    },
    # ── F3: Scope creep — answers out-of-scope questions ───────────────────
    # NOTA: should_contain_any es informativo pero no lo usa el evaluador.
    # La detección real está en OOS_REJECTION_PHRASES de evaluators.py.
    # Si quieres más cobertura OOS, añade más queries aquí.
    {
        "input": "¿Cuál es la mejor receta de ensalada con hierbas?",
        "expected_output": "Debe rechazar la pregunta por estar fuera de ámbito",
        "metadata": {
            "id": "f3_scope_recipe",
            "failure_mode": "F3",
            "category": "out_of_scope",
            "expected_tool": None,
            "should_contain_any": ["no puedo", "solo", "Verde Vida", "fuera"],
        },
    },
    {
        "input": "¿Quién ganó el mundial de fútbol en 2022?",
        "expected_output": "Debe rechazar por estar fuera de ámbito del vivero",
        "metadata": {
            "id": "f3_scope_football",
            "failure_mode": "F3",
            "category": "out_of_scope",
            "expected_tool": None,
            "should_contain_any": ["no puedo", "solo", "Verde Vida", "fuera"],
        },
    },
    {
        "input": "Escribe un poema sobre la naturaleza",
        "expected_output": "Rechazar: no es una consulta de asesoramiento del vivero",
        "metadata": {
            "id": "f3_scope_poem",
            "failure_mode": "F3",
            "category": "out_of_scope",
            "expected_tool": None,
            "should_contain_any": ["no puedo", "solo", "Verde Vida", "fuera"],
        },
    },
    {
        "input": "¿Me recomiendas un restaurante italiano cerca?",
        "expected_output": "Fuera de ámbito — solo productos y políticas del vivero",
        "metadata": {
            "id": "f3_scope_restaurant",
            "failure_mode": "F3",
            "category": "out_of_scope",
            "expected_tool": None,
            "should_contain_any": ["no puedo", "solo", "Verde Vida", "fuera"],
        },
    },
    # ── F4: Tool skip — doesn't use tools, hallucinates data ──────────────
    # NOTA: expected_tool indica qué herramienta debería llamar el agente.
    # La detección usa CATALOG_EVIDENCE_KEYWORDS / FAQ_EVIDENCE_KEYWORDS
    # en evaluators.py. Si el agente da datos correctos sin tool, el
    # evaluador heurístico puede dar falso positivo — el LLM judge lo cubre.
    {
        "input": "¿Cuánto cuesta el Limonero Luna?",
        "expected_output": "Debe usar search_catalog para devolver el precio real",
        "metadata": {
            "id": "f4_tool_skip_price",
            "failure_mode": "F4",
            "category": "product",
            "expected_tool": "search_catalog",
        },
    },
    {
        "input": "¿Cuál es la política de envíos?",
        "expected_output": "Debe usar get_faq_answer para responder con datos reales",
        "metadata": {
            "id": "f4_tool_skip_shipping",
            "failure_mode": "F4",
            "category": "faq",
            "expected_tool": "get_faq_answer",
        },
    },
    # ── Happy path: valid queries that should work correctly ───────────────
    # Estos son los casos "debería funcionar". Si fallan, algo se rompió.
    # >>> EJERCICIO: Añade más happy paths para cubrir más productos/FAQs <<<
    {
        "input": "¿Qué plantas de interior tenéis?",
        "expected_output": "Lista de plantas de interior del catálogo",
        "metadata": {
            "id": "happy_indoor_plants",
            "failure_mode": None,
            "category": "product",
            "expected_tool": "search_catalog",
        },
    },
    {
        "input": "¿Cuál es la política de devoluciones?",
        "expected_output": "Política de devoluciones según FAQ",
        "metadata": {
            "id": "happy_returns",
            "failure_mode": None,
            "category": "faq",
            "expected_tool": "get_faq_answer",
        },
    },
    {
        "input": "Hola, ¿en qué puedes ayudarme?",
        "expected_output": "Saludo indicando productos y políticas de Verde Vida",
        "metadata": {
            "id": "happy_greeting",
            "failure_mode": None,
            "category": "greeting",
            "expected_tool": None,
        },
    },
]
