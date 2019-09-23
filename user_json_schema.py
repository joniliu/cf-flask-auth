from jsonschema import validate
from jsonschema.exceptions import SchemaError
from jsonschema.exceptions import ValidationError

user_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 5
        }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'status': False, 'message': e}
    except SchemaError as e:
        return {'status': False, 'message': e}
    return {'status': True, 'data': data}
