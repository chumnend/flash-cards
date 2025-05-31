from pyramid.view import view_config


@view_config(route_name='home', renderer='flashly:templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'flashly'}


@view_config(route_name='status', renderer='json')
def status(request):
    return {'message': 'OK'}

