from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str()
    user_id = fields.Int(required=True)
