
def test_ready(client):
    response = client.get('/')
    
    assert response.status_code == 200
    data = response.json
    assert data['status'] == 'ready'
    assert 'time' in data