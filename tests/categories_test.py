import pytest
# для тестирования редис импортировал данный модуль, позволяющий подменять объекты для теста
from unittest.mock import patch
from limiter import limiter

# чтобы не было конфликта при тесте
limiter.enabled = False


# тест создания категорий
@pytest.mark.asyncio
async def test_create_category(auth_client):
    response = await auth_client.post('/categories', json={'name': 'test_category', 'description': 'text'})

    assert response.status_code == 201
    assert response.json()['name'] == 'test_category'


# тест выведения списка категорий пользователя
@pytest.mark.asyncio
async def test_get_list_of_categories(auth_client):
    await auth_client.post(url='/categories', json={'name': 'cat_1', 'description': 'text'})
    await auth_client.post(url='/categories', json={'name': 'cat_2'})

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


# тест проверки кеша
@pytest.mark.asyncio
async def test_get_categories_from_cache(auth_client, fake_redis_client):
    # данная команда позволяет в services/categories заменить redis_client на фейковый клиент
    with patch('services.categories.redis_client', fake_redis_client):
        await auth_client.post(url='/categories', json={'name': 'cat_1', 'description': 'text'})
        await auth_client.post(url='/categories', json={'name': 'cat_2'})
        r_user = await auth_client.get(url='/me')
        user_id = r_user.json()['id']

        r1 = await auth_client.get(url='/categories')
        cached = await fake_redis_client.get(f'categories:{user_id}')
        r2 = await auth_client.get(url='/categories')

    assert r1.status_code == 200
    assert cached is not None
    assert r1.json()[0]['name'] == 'cat_1'
    assert r2.json()[1]['name'] == 'cat_2'
