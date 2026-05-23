import pytest
from limiter import limiter

# чтобы не было конфликта при тесте
limiter.enabled = False


# тест создания категорий
@pytest.mark.asyncio
async def test_create_transaction(auth_client):
    create_category = await auth_client.post('/categories', json={'name': 'test_category', 'description': 'text'})

    response = await auth_client.post(url='/transactions', json={
        'amount': 9999.99,
        'description': 'food',
        'type': 'expense',
        'category_id': f'{create_category.json()['id']}'
    })

    assert create_category.status_code == 201
    assert response.status_code == 201
    assert response.json()['id'] == 1


# тест получения транзакций по фильтрам
@pytest.mark.asyncio
async def test_filter_transactions(auth_client):
    c1 = await auth_client.post('/categories', json={'name': 'c1', 'description': 'text'})
    c2 = await auth_client.post('/categories', json={'name': 'c2', 'description': 'text'})

    t1 = await auth_client.post(url='/transactions', json={
        'amount': 9999.99,
        'type': 'expense',
        'category_id': f'{c1.json()['id']}'
    })
    t2 = await auth_client.post(url='/transactions', json={
        'amount': 9999.99,
        'type': 'expense',
        'category_id': f'{c1.json()['id']}'
    })
    t3 = await auth_client.post(url='/transactions', json={
        'amount': 9999.99,
        'type': 'expense',
        'category_id': f'{c2.json()['id']}'
    })

    params = {'category_id': f'{c1.json()['id']}'}

    r = await auth_client.get('/transactions', params=params)

    assert c1.status_code == 201
    assert c2.status_code == 201
    assert t1.status_code == 201
    assert t2.status_code == 201
    assert t3.status_code == 201
    assert r.status_code == 200
    assert isinstance(r.json(), list)


# тест получения транзакции по id
@pytest.mark.asyncio
async def test_get_transaction(auth_client):
    c1 = await auth_client.post('/categories', json={'name': 'c44', 'description': 'text'})
    assert c1.status_code == 201

    t1 = await auth_client.post(url='/transactions', json={
        'amount': 9999.99,
        'type': 'expense',
        'category_id': c1.json()['id']
    })
    assert t1.status_code == 201

    r = await auth_client.get(f'/transaction/{t1.json()['id']}')

    assert r.status_code == 200
    assert r.json()['amount'] == '9999.99'
