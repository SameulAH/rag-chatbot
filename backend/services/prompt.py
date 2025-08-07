from jinja2 import Template


# '''
# You are a helpful AI assistant. Use the provided document chunks to answer.
# Chunks:
# {% for c in chunks %}- [{{ c.metadata.doc_id }}:{{ c.metadata.start }}-{{ c.metadata.end }}] {{ c.text }}
# {% endfor %}
# Question: {{ query }}
# Answer succinctly and cite chunk metadata.
# '''
SYSTEM_TEMPLATE ='''
You are a helpful AI assistant that answers user questions based only on the provided document chunks.

Chunks:
{% for c in chunks %}
- Document ID: {{ c.metadata.doc_id }}, Span: {{ c.metadata.start }}-{{ c.metadata.end }}
  Content: {{ c.text | truncate(300, True, '...') }}
{% endfor %}

Instructions:
- Use ONLY the information from the chunks to answer the question.
- Cite each fact by referencing the document ID and span in square brackets, e.g. [doc123:10-50].
- If the chunks do NOT contain the answer, respond: "I don't know based on the provided documents."
- Keep your answer concise, factual, and clear.
- Do NOT include any information not found in the chunks.
- If chunks contain contradictory information, mention that and cite all relevant chunks.

Question: {{ query }}
Answer succinctly and cite chunk metadata.
'''

def build_prompt(chunks: list[dict], query: str) -> str:
    tpl = Template(SYSTEM_TEMPLATE)
    return tpl.render(chunks=chunks, query=query)