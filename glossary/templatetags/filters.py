from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.filter
def highlight(text, query):
    """
    텍스트에서 검색어를 강조 표시합니다.
    """
    if not query:
        return text
    highlighted = text.replace(query, f'<mark>{query}</mark>')
    return mark_safe(highlighted)
