from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def truncate_words_html(value, arg):
    """
    Truncates HTML after a certain number of words, preserving HTML tags
    """
    if not value:
        return ""
    
    try:
        length = int(arg)
    except ValueError:
        return value
    
    # Simple word counting that ignores HTML tags
    import re
    text_content = re.sub(r'<[^>]*>', '', str(value))
    words = text_content.split()
    
    if len(words) <= length:
        return value
    
    # Find the position after the nth word in the original HTML
    word_count = 0
    result = ""
    i = 0
    in_tag = False
    
    while i < len(value) and word_count < length:
        char = value[i]
        result += char
        
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
        elif not in_tag and char.isspace():
            # Count words only outside of tags
            if i + 1 < len(value) and not value[i + 1].isspace():
                word_count += 1
        
        i += 1
    
    return mark_safe(result + "...")

@register.filter  
def add_class(field, css_class):
    """Add CSS class to form field"""
    return field.as_widget(attrs={"class": css_class})
