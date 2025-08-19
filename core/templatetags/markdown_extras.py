from django import template
from django.utils.safestring import mark_safe
import markdown
import re

register = template.Library()

@register.filter
def markdown_to_html(value):
    """Convert markdown text to HTML"""
    if not value:
        return ""
    
    # Configure markdown with extensions
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br',
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'css_class': 'highlight',
                'use_pygments': False,
            }
        }
    )
    
    # Convert markdown to HTML
    html = md.convert(value)
    
    # Add custom classes to elements for better styling
    html = re.sub(r'<h1>', '<h1 class="text-4xl font-bold mb-8 mt-12 bg-clip-text text-transparent bg-gradient-to-r from-gray-800 to-black">', html)
    html = re.sub(r'<h2>', '<h2 class="text-3xl font-bold mb-6 mt-10 text-gray-900">', html)
    html = re.sub(r'<h3>', '<h3 class="text-2xl font-semibold mb-4 mt-8 text-gray-900">', html)
    html = re.sub(r'<p>', '<p class="text-lg leading-relaxed mb-6 text-gray-600">', html)
    html = re.sub(r'<ul>', '<ul class="list-disc list-inside space-y-3 mb-6">', html)
    html = re.sub(r'<ol>', '<ol class="list-decimal list-inside space-y-3 mb-6">', html)
    html = re.sub(r'<li>', '<li class="text-gray-600">', html)
    html = re.sub(r'<blockquote>', '<blockquote class="border-l-4 border-black pl-4 italic my-6 text-gray-700 bg-gray-50 py-2 px-4 rounded-r-lg">', html)
    html = re.sub(r'<pre>', '<pre class="bg-gray-900 text-gray-100 p-4 my-6 overflow-x-auto rounded-lg" style="box-shadow: 0 4px 10px rgba(0,0,0,0.1);">', html)
    html = re.sub(r'<code>', '<code class="bg-gray-100 rounded px-1 py-0.5 text-black">', html)
    html = re.sub(r'<img([^>]*)>', r'<img\1 class="w-full h-auto rounded-xl shadow-lg my-8" style="box-shadow: 0 10px 30px rgba(0,0,0,0.1);">', html)
    html = re.sub(r'<a([^>]*)>', r'<a\1 class="text-black font-medium hover:underline">', html)
    
    return mark_safe(html)
