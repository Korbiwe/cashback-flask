from jsonschema import Draft7Validator

schema = {
    'type': 'object',
    'properties': {
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
    'required': ['individual_taxpayer_number', 'official_name']
}
Draft7Validator.check_schema(schema)
