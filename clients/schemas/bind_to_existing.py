from jsonschema import Draft7Validator

schema = {
    'type': 'object',
    'properties': {
        'fullname': {
            'type': 'string'
        },
    },
    'additional_properties': False,
    'required': ['fullname']
}
Draft7Validator.check_schema(schema)
