import re
from django import template
from basic.blog.models import Post

register = template.Library()

class PostArchive(template.Node):
    def __init__(self, var_name, scale="month"):
        self.var_name = var_name
        self.scale = scale

    def render(self, context):
        dates = Post.objects.published().dates('publish', self.scale, order='DESC')
        if dates:
            context[self.var_name] = dates
        return ''

@register.tag
def get_post_archive_months(parser, token):
    """Populates the current context with a list of the unique months in the archive"""
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    var_name = m.groups()[0]
    return PostArchive(var_name)

get_post_archive = get_post_archive_months

@register.tag
def get_post_archive_years(parser, token):
    """Populates the current context with a list of the unique years in the archive"""
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    var_name = m.groups()[0]
    return PostArchive(var_name, scale="year")

