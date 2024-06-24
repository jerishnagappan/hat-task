

from marshmallow import Schema, fields, validate

class InventorNameSchema(Schema):
    inventor_name = fields.Str(required=True, validate=validate.Length(max=255))


class PatentSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=255))
    application_number = fields.Str(validate=validate.Length(max=255))
    inventor_name = fields.List(fields.Nested(InventorNameSchema), required=True)
    assignee_name_orig = fields.Str(validate=validate.Length(max=255))
    assignee_name_current = fields.Str(validate=validate.Length(max=255))
    pub_date = fields.Date(format='%Y-%m-%d')  
    filing_date = fields.Date(format='%Y-%m-%d')
    priority_date = fields.Date(format='%Y-%m-%d')
    grant_date = fields.Date(format='%Y-%m-%d')
    forward_cites_no_family = fields.Dict()
    forward_cites_yes_family = fields.Dict()
    backward_cites_no_family = fields.Dict()
    backward_cites_yes_family = fields.Dict()
    patnum = fields.Str(required=True, validate=validate.Length(max=255))
    abstract= fields.Str(required=True, validate=validate.Length(max=1250),nullable =True)















# from marshmallow import Schema, fields, validate

# class PatentSchema(Schema):
#     id = fields.Int(dump_only=True)
#     title = fields.Str(required=True, validate=validate.Length(max=255))
#     application_number = fields.Str(required=False, validate=validate.Length(max=255))
#     inventor_name = fields.List(fields.Str())  
#     assignee_name_orig = fields.List(fields.Dict())  
#     assignee_name_current = fields.List(fields.Dict())  # Assuming it's a list of dictionaries
#     pub_date = fields.Str(validate=validate.Length(max=255))
#     filing_date = fields.Str(validate=validate.Length(max=255))
#     priority_date = fields.Str(validate=validate.Length(max=255))
#     grant_date = fields.Str(validate=validate.Length(max=255))
#     forward_cites_no_family = fields.Dict()
#     forward_cites_yes_family = fields.Dict()
#     backward_cites_no_family = fields.Dict()
#     backward_cites_yes_family = fields.Dict()
#     patnum = fields.Str(required=True, validate=validate.Length(max=255))






# class PatentSchema(Schema):
#     id = fields.Int(dump_only=True)
#     title = fields.Str(required=True, validate=validate.Length(max=255))
#     application_number = fields.Str(validate=validate.Length(max=255))
#     inventor_name = fields.List(fields.Nested(InventorNameSchema), required=True)  
#     assignee_name_orig = fields.Str(validate=validate.Length(max=255))
#     assignee_name_current = fields.Str(validate=validate.Length(max=255))
#     pub_date = fields.Str(validate=validate.Length(max=255))
#     filing_date = fields.Str(validate=validate.Length(max=255))
#     priority_date = fields.Str(validate=validate.Length(max=255))
#     grant_date = fields.Str(validate=validate.Length(max=255))
#     forward_cites_no_family = fields.Dict()
#     forward_cites_yes_family = fields.Dict()
#     backward_cites_no_family = fields.Dict()
#     backward_cites_yes_family = fields.Dict()
#     patnum = fields.Str(required=True, validate=validate.Length(max=255))
