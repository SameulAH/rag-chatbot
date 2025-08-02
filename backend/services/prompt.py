from jinja2 import Template

SYSTEM_TEMPLATE = '''
You are a helpful AI assistant. Use the provided document chunks to answer.
Chunks:
{% for c in chunks %}- [{{ c.metadata.doc_id }}:{{ c.metadata.start }}-{{ c.metadata.end }}] {{ c.text }}
{% endfor %}
Question: {{ query }}
Answer succinctly and cite chunk metadata.
'''

def build_prompt(chunks: list[dict], query: str) -> str:
    tpl = Template(SYSTEM_TEMPLATE)
    return tpl.render(chunks=chunks, query=query)