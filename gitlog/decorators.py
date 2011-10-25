###########################################
# http://djangosnippets.org/snippets/559/ #
###########################################


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def auto_render(func):
    """Decorator that automaticaly call the render_to_response shortcut.

    The view must return a tuple with two items : a template filename and the desired context.
    HttpResponse object could be also returned. it's possible to override the default 
    template filename by calling a decorated view with an "template_name" parameter
    or to get only the context dictionary via "only_context" parameter.

    >>> from utils.utils import auto_render
    >>> @auto_render
    ... def test(request):
    ...     return 'base.html', {'oki':1}
    ...
    >>> from django.http import HttpRequest, HttpResponse
    >>> response = test(HttpRequest())
    >>> assert type(response) is HttpResponse
    >>> response = test(HttpRequest(), only_context=True)
    >>> assert response['oki'] == 1
    >>> try:
    ...     response = test(HttpRequest(), template_name='fake_template.html')
    ... except Exception, e:
    ...     e.message
    'fake_template.html'
    """

    def _dec(request, *args, **kwargs):

        if kwargs.get('only_context', False):
            # return only context dictionary
            del(kwargs['only_context'])
            response = func(request, *args, **kwargs)
            if isinstance(response, HttpResponse) or isinstance(response, HttpResponseRedirect):
                raise Exception("cannot return context dictionary because a HttpResponseRedirect as been found")
            (template_name, context) = response
            return context

        if kwargs.get('template_name', False):
            overriden_template_name = kwargs['template_name']
            del(kwargs['template_name'])
        else:
            overriden_template_name = None

        response = func(request, *args, **kwargs)

        if isinstance(response, HttpResponse) or isinstance(response, HttpResponseRedirect):
            return response
        (template_name, context) = response
        if overriden_template_name:
            template_name = overriden_template_name

        return render_to_response(template_name, context, context_instance=RequestContext(request))
    return _dec