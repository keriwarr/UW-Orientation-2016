from django import template
from django.template.defaultfilters import stringfilter

import re

register = template.Library()

@register.filter(name='youtube_embed')
@stringfilter
def youtube_embed(url):
    """Converts a given YouTube URL into an embeddable URL"""

    match = re.search(r'(v=|youtu.be/)([^&]+)', url)
    if match:
        video_id = match.group(2)
        return "https://www.youtube.com/embed/%s" % video_id
    return url
