
from marshmallow import Schema, fields, validate

class PatentSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=255))
    application_number = fields.Str(required=True, validate=validate.Length(max=255))
    inventor_name = fields.Dict()
    assignee_name_orig = fields.Dict()
    assignee_name_current = fields.Dict()
    pub_date = fields.Str(validate=validate.Length(max=255))
    filing_date = fields.Str(validate=validate.Length(max=255))
    priority_date = fields.Str(validate=validate.Length(max=255))
    grant_date = fields.Str(validate=validate.Length(max=255))
    forward_cites_no_family = fields.Dict()
    forward_cites_yes_family = fields.Dict()
    backward_cites_no_family = fields.Dict()
    backward_cites_yes_family = fields.Dict()
