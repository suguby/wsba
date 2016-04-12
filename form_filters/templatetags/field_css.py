# -*- coding: utf-8 -*-
import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


class CssChanger:
    # <input class="vTextField" id="id_name" maxlength="64" name="name" type="text" />

    def __init__(self):
        self._re_tag_begin = re.compile(r'^(\s*<\w+)\s+')
        self._re_css_class = re.compile(r'\s+class="(.*?)"\s*')

    def add(self, matched, elem, klass):
        pos = matched.end(1)
        elem = '{} {}{}'.format(elem[:pos], klass, elem[pos:])
        return elem

    def replace(self, matched, elem, klass):
        elem = '{}{}{}'.format(elem[:matched.start(1)], klass, elem[matched.end(1):])
        return elem

    def do(self, elem, klass, action):
        elem = str(elem)
        matched = self._re_css_class.search(elem)
        if matched:
            return action(matched, elem, klass)
        else:
            matched = self._re_tag_begin.search(elem)
            if not matched:
                return elem
            pos = matched.end(1)
            elem = u'{} class="{}"{}'.format(elem[:pos], klass, elem[pos:])
            return elem

_css_changer = CssChanger()


@register.filter(is_safe=True)
@stringfilter
def add_css_class(elem, klass):
    return _css_changer.do(elem, klass, _css_changer.add)


@register.filter(is_safe=True)
@stringfilter
def replace_css_class(elem, klass):
    return _css_changer.do(elem, klass, _css_changer.replace)

