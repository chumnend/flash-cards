from pyramid.view import view_config
from pyramid.view import notfound_view_config


@view_config(route_name='home', renderer='flashly:templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'flashly'}


@view_config(route_name='status', renderer='json')
def status(request):
    return {'message': 'OK'}


@notfound_view_config(renderer='flashly:templates/404.jinja2')
def notfound_view(request):
    request.response.status = 404
    return {}
