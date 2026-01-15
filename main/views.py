from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

from .services import MC


def index(request):
    context = {
        'title': 'Главная',
        'flen': len(MC.full_moons),
    }
    return render(request, 'main/index.html', context)


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))
