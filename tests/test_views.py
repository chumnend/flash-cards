from flashly.views.default import my_view
from flashly.views.default import status
from flashly.views.default import notfound_view


def test_my_view(app_request):
    info = my_view(app_request)
    assert app_request.response.status_int == 200
    assert info['project'] == 'flashly'

def test_notfound_view(app_request):
    info = notfound_view(app_request)
    assert app_request.response.status_int == 404
    assert info == {}

def test_status_view(app_request):
    info = status(app_request)
    assert app_request.response.status_int == 200
    assert info['message'] == 'OK'
