import asyncio
import time

import pytest
from httpx import AsyncClient

from src.app import app


filed_name_id = time.time()


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def client():
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.mark.parametrize(
    'data, answer',
    [
        (
                {
                    'email': 'example@gmail.com',
                    'phone': '+7 123 322 25 56',
                    'date': '2023-02-21',
                    'bio': 'Lorem ipsum'
                },
                {
                    'name': 'Settings form'
                }
        ),
        (
                {
                    'user_email': 'example@gmail.com',
                    'user_phone': '+7 123622 25 56',
                    'user_name': 'Lorem ipsum',
                    'user_nameaaaa': 'Lorem ipsum'
                },
                {
                    'name': 'Account form'
                }
        ),
        (
                {
                    'user_email': 'example@gmail.com',
                    'user_phone': '+7 123622 aa 56',
                    'user_name': 'Lorem ipsum'
                },
                {
                    'user_email': 'email',
                    'user_phone': 'str',
                    'user_name': 'str'
                }
        ),
        (
                {
                    'user_aa': 'example.com',
                    'user_ps': '+7 123622 aa 56',
                    'asd': 'Lorem ipsum',
                    'phone': '+71236222556'
                },
                {
                    'user_aa': 'str',
                    'user_ps': 'str',
                    'asd': 'str',
                    'phone': 'phone'
                }
        ),
        (
                {},
                {}
        )
    ]
)
async def test_get_form(
        client: AsyncClient,
        data,
        answer
):
    response = await client.post('/get_form', json=data)
    assert response.status_code == 200
    assert response.json() == answer


@pytest.mark.parametrize(
    'data, answer, status',
    [
        (
                {
                    'template_name': f'Field form{filed_name_id}',
                    'f_name': 'field name',
                    'f_phone': '+7 123321 1222',
                    'f_email': 'email@gamil.com'
                },
                {
                    'template_name': f'Field form{filed_name_id}',
                    'f_name': 'str',
                    'f_phone': 'phone',
                    'f_email': 'email'
                },
                201
        ),
        (
                {
                    'template_name': 'example form',
                    'field_1_name': 'field_1_type',
                    'field_2_name': 'field_2_type',
                    'field_3_name': 'field_3_type',
                    '...': '...'
                },
                {
                    "detail": "Don't send example data!"
                },
                400
        ),
        (
                {
                    'template_name': 'Field form',
                    'f_name': 'field name',
                    'f_phone': '+7 123321 1222',
                    'f_email': 'email@gamil.com',
                    'bio': 'bio information'
                },
                {
                    "detail": "Form with template_name: Field form is already exists!"
                },
                400
        ),
        (
                {
                    'template_name': 'Field form',
                },
                {
                    "detail": "Empty form data!"
                },
                400
        )
    ]
)
async def test_create_form(
        client: AsyncClient,
        data,
        answer,
        status
):
    template_name = data.pop('template_name')
    response = await client.post(
        f'/create_form',
        params={'template_name': template_name},
        json=data
    )

    assert response.status_code == status
    assert response.json() == answer
