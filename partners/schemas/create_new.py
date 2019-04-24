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
        'individual_taxpayer_number': {
            'type': 'string',
            'pattern': "^\d{10}|\d{12}$"
        },
        'display_name': {
            'type': 'string'
        },
        'official_name': {
            'type': 'string'
        }
    },
    'additional_properties': False,
    'required': ['individual_taxpayer_number', 'official_name', 'password', 'phone', 'email', 'login']
}
Draft7Validator.check_schema(schema)
