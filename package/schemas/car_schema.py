from marshmallow import Schema, fields, validate


class CarSchema(Schema):
    id = fields.Int(dump_only=True)
    brand = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    model = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    user_id = fields.Int(required=True)
