import datetime
import re

from django import template

from basic.blog.models import Post

register = template.Library()

class PostArchive(template.Node):
    def __init__(self, var_name, scale="month", year=None):
        self.var_name = var_name
        self.scale    = scale
        self.year     = template.Variable(year) if year else None

    def render(self, context):
        posts = Post.objects.published()

        if self.year:
            year = int(self.year.resolve(context))
        else:
            year = datetime.datetime.now().year

        posts = posts.filter(publish__year=year)

        dates = posts.dates('publish', self.scale, order='DESC')

        if dates:
            context[self.var_name] = dates

        return ''

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

@register.tag
def get_post_archive_months(parser, token):
    """
    Populates the current context with a list of the unique months in the archive

    Usage:

        {% get_post_archive_months as months %}
        {% get_post_archive_months for year as months %}
        {% get_post_archive_months for "2008" as months %}

    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]

    m = re.search(r'(|for (?P<year>["\w]+) )as (?P<var_name>\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag must be called as: for <year> as <var_name>" % tag_name

    groups = m.groupdict()

    var_name = groups["var_name"]
    year = groups.get("year", None)
    return PostArchive(var_name, year=year)

get_post_archive = get_post_archive_months

