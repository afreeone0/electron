from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string


def index(request):
    context = {

    }
    return render(request, 'store/index.html', context=context)


def page_not_found(request, exception):
    template404 = render_to_string('page_not_found.html')
    return HttpResponseNotFound(template404)
