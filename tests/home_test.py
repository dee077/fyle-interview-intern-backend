from core.libs.exceptions import FyleError

def test_ready(client):
    response = client.get('/')
    
    assert response.status_code == 200
    data = response.json
    assert data['status'] == 'ready'
    assert 'time' in data

def test_page_not_found(client):
    response = client.get('/any-endpoint')
    assert response.status_code == 404
    assert response.json['error'] == 'NotFound'

def test_fyle_error_to_dict():
    error_message = "This is a test error message"
    status_code = 404
    error = FyleError(status_code=status_code, message=error_message)
    
    error_dict = error.to_dict()
    
    assert error_dict == {'message': error_message}
    assert error.status_code == status_code