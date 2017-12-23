address_validation_schema = {
    "type": "object",
    "properties": {
        "address": {"type": "string", "minLength": 81}
    },
    "required": [
        "address"
    ]
}
