import enum

from fastapi import FastAPI, Body, HTTPException, status
from tinydb import TinyDB, Query

from src.utils import get_data_template, check_data_compliance, validate_data

app = FastAPI()
db = TinyDB('db.json')


class DateTypes(enum.Enum):
    date_1 = 'YYYY-MM-DD'
    date_2 = 'DD.MM.YYYY'


class FormTypes(enum.Enum):
    email: str = 'email'
    phone: str = 'phone'
    date: DateTypes = DateTypes.date_1
    text: str = 'str'


request_example = {
    'field_1_name': 'field_1_type',
    'field_2_name': 'field_2_type',
    'field_3_name': 'field_3_type',
    '...': '...',
}

responses = {
    200: {
        "content": {
            "application/json": {
                "example": {
                    'form_is_found': {'name': 'Form template name'},
                    'form_not_found': request_example
                }
            }
        },
    },
}


@app.post("/get_form", responses=responses)
async def get_form(data: dict = Body(default=request_example)):
    db_data = db.table('_default').all()
    form_template = await get_data_template(
        request_data=data,
        db_data=db_data
    )

    return await check_data_compliance(
        actual_data=data,
        template_data=form_template
    )


@app.post(
    '/create_form',
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": request_example
                }
            },
        }
    }
)
async def create_form(
        template_name: str,
        data: dict = Body(default=request_example)
):
    if not len(data):
        raise HTTPException(
            detail='Empty form data!',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if data == request_example:
        raise HTTPException(
            detail="Don't send example data!",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if db.search(Query().template_name == template_name):
        raise HTTPException(
            detail=f'Form with template_name:'
                   f' {template_name} is already exists!',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    validated_data = await validate_data(data)
    validated_data['template_name'] = template_name
    db.insert(validated_data)

    return validated_data
