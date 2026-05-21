import pytest


# тест создания категорий
@pytest.mark.asyncio
async def test_create_category(auth_client):
    response = await auth_client.post('/categories', json={'name': 'test_category', 'description': 'text'})

    assert response.status_code == 201
    assert response.json()['name'] == 'test_category'


# тест выведения списка категорий пользователя
@pytest.mark.asyncio
async def test_get_list_of_categories(auth_client):
    query = await auth_client.post(url='/categories', json={'name': 'cat_1', 'description': 'text'})
    query_2 = await auth_client.post(url='/categories', json={'name': 'cat_2'})

    response = await auth_client.get(url='/categories')

    assert response.status_code == 200
    assert response.json()[0]['name'] == 'cat_1'
    assert response.json()[1]['name'] == 'cat_2'


# тест удаления категории
@pytest.mark.asyncio
async def test_delete_category(auth_client):
    request = await auth_client.post(url='/categories', json={'name': 'cat_1', 'description': 'text'})
    delete_request = await auth_client.delete(url=f'/categories/{request.json()['id']}')
    check_deleteed = await auth_client.get(url=f'/categories/{request.json()['id']}')

    assert request.status_code == 201
    assert delete_request.status_code == 200
    assert check_deleteed.status_code == 404
