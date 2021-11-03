from django import template
from ..models import Category, Article
from ..filter import ProductFilter
from django.db.models import Min, Max
from django.shortcuts import render

register = template.Library()


@register.inclusion_tag('blog/partials/category_navbar.html')
def category_navbar():
    return {
        'category': Category.objects.filter(status=True)
    }


@register.simple_tag()
def filter_url(number, name, urlencode=None):
    url = '?{}={}'.format(name, number)
    if urlencode:
        sp_query = urlencode.split('&')
        sp_filter = filter(lambda x: x.split('=')[0] != name, sp_query)
        join_query = '&'.join(sp_filter)
        url = '{}&{}'.format(url, join_query)
        return url
