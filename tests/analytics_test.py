import pytest
from limiter import limiter

limiter.enabled = False


# тест запроса на статистику по категориям
@pytest.mark.asyncio
async def test_get_category_analytics(auth_client):
    c1 = await auth_client.post(url='/categories', json={'name': 'cat_1'})
    c2 = await auth_client.post(url='/categories', json={'name': 'cat_2'})
    await auth_client.post(url='/transactions', json={
        'amount': 9999.99,
        'type': 'expense',
        'category_id': f'{c1.json()['id']}'
    })
    await auth_client.post(url='/transactions', json={
        'amount': 9999.99,
        'type': 'expense',
        'category_id': f'{c2.json()['id']}'
    })

    g_a = await auth_client.get(f'/category/analytics')

    assert g_a.status_code == 200
    assert isinstance(g_a.json(), list)


# тест запроса ежемесячной аналитики
@pytest.mark.asyncio
async def test_get_monthly_analytics(auth_client):
    c1 = await auth_client.post(url='/categories', json={'name': 'cat_1'})
    await auth_client.post(url='/transactions', json={
        'amount': 9999.99,
        'type': 'expense',
        'date': '2026-04-01',
        'category_id': f'{c1.json()['id']}'
    })
    await auth_client.post(url='/transactions', json={
        'amount': 9999.99,
        'type': 'expense',
        'date': '2026-05-01',
        'category_id': f'{c1.json()['id']}'
    })

    g_a = await auth_client.get(f'/monthly')

    assert g_a.status_code == 200
    assert isinstance(g_a.json(), list)
