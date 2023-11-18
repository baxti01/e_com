from src.validators import run_validators


async def get_data_template(request_data: dict, db_data: list[dict]) -> dict:
    result = {}
    for index, document in enumerate(db_data):
        document_copy = document.copy()
        document_copy.pop('template_name', None)
        if set(document_copy.keys()) <= set(request_data.keys()):
            if len(result) < len(document):
                result = document

    return result


async def check_data_compliance(
        actual_data: dict,
        template_data: dict
) -> dict:
    print(template_data)
    form_name = template_data.pop('template_name', None)
    answer = len(template_data)

    for key in actual_data:
        actual_data_field_type = await run_validators(actual_data[key])
        actual_data[key] = actual_data_field_type
        db_field = template_data.get(key, None)

        if db_field and answer:
            answer = template_data[key] == actual_data_field_type

    if answer:
        return {'name': form_name}

    return actual_data


async def validate_data(data: dict) -> dict:
    for key in data:
        data[key] = await run_validators(data[key])

    return data
