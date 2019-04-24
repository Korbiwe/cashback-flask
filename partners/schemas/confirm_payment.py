from jsonschema import Draft7Validator

schema = {
    'type': 'object',
    'properties': {
        'request_id': {
            'type': 'number',
            'minimum': 1
        },
        'code': {
            'type': 'string'
        }
    },
    'additional_properties': False,
    'required': ['request_id', 'code']
}
Draft7Validator.check_schema(schema)
