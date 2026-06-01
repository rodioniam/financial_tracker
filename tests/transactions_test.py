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


# тест обновления транзакции
@pytest.mark.asyncio
async def test_update_transaction(auth_client):
    p_c = await auth_client.post('/categories', json={'name': 'test_category', 'description': 'text'})
    p_c2 = await auth_client.post('/categories', json={'name': 'test_category_2', 'description': 'text'})
    assert p_c.status_code == 201
    assert p_c2.status_code == 201

    p_t = await auth_client.post(url='/transactions', json={
        'amount': 9999.99,
        'description': 'food',
        'date': '2025-01-01',
        'type': 'expense',
        'category_id': f'{p_c.json()['id']}'
    })

    assert p_t.status_code == 201
    assert p_t.json()['category_id'] == p_c.json()['id']

    patch_t = await auth_client.patch(f"/transactions/{p_t.json()['id']}", json={
        'amount': 10000,
        'date': '2026-12-12',
        'category_id': f"{p_c2.json()['id']}"
    })

    assert patch_t.status_code == 200
    assert patch_t.json()['id'] == p_t.json()['id']
    assert patch_t.json()['amount'] != p_t.json()['amount']
    assert patch_t.json()['amount'] == '10000'
    assert patch_t.json()['date'] != p_t.json()['date']
    assert patch_t.json()['category_id'] != p_t.json()['category_id']


# тест удаления транзакции
@pytest.mark.asyncio
async def test_delete_transaction(auth_client):
    p_c = await auth_client.post('/categories', json={'name': 'test_category', 'description': 'text'})
    assert p_c.status_code == 201

    p_t = await auth_client.post(url='/transactions', json={
        'amount': 9999.99,
        'description': 'food',
        'date': '2025-01-01',
        'type': 'expense',
        'category_id': f'{p_c.json()['id']}'
    })
    assert p_t.status_code == 201

    d_t = await auth_client.delete(f"/transactions/{p_t.json()['id']}")
    check_deleted = await auth_client.get(f"/transaction/{p_t.json()['id']}")
    assert d_t.status_code == 200
    assert check_deleted.status_code == 404
