from django import template

from users.roles import (FOC, MOD, HEAD_LEADER)

register = template.Library()

@register.filter
def can_edit_team_settings(user):
    return user.position in list((FOC, MOD, HEAD_LEADER))

@register.filter
def as_html(text):
    repls = (
        ('\n', '<br/>'),
        ('<style>', ''),
        ('<style/>', ''),
        ('<link>', ''),
        ('</link>', ''),
        ('<script>', ''),
        ('<script/>', ''),
    )
    for orig, new in repls:
        text = text.replace(orig, new)
    return text
