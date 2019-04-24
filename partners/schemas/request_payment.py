from jsonschema import Draft7Validator


schema = {
    'type': 'object',
    'properties': {
        'amount': {
            'type': 'number',
            'minimum': 1,
        },
        'description': {
            'type': 'string'
        },
        'credential': {
            'type': 'string'
        }
    },
    'additional_properties': False,
    'required': ['amount', 'credential']
}
Draft7Validator.check_schema(schema)
