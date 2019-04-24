from jsonschema import Draft7Validator

schema = {
    'type': 'object',
    'properties': {
        'login': {
            'type': 'string',
            'pattern': '^[a-zA-Z0-9]+'
        },
        'phone': {
            'type': 'string',
            'pattern': '^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$'
        },
        'email': {
            'type': 'string',
            'format': 'email',
        },
        'password': {
            'type': 'string'
        },
        'fullname': {
            'type': 'string'
        },
    },
    'additional_properties': False,
    'required': ['password', 'phone', 'email', 'login', 'fullname']
}
Draft7Validator.check_schema(schema)
