"""
Render text into Markdown.
"""

import markdown


EXTENSIONS = ['extra', 'toc']
SAFE_MODE = 'escape'


def render(content):
    return markdown.markdown(content,
            extensions=EXTENSIONS,
            output_format='html5',
            safe_mode=SAFE_MODE)
