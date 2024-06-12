from marshmallow import Schema, fields

class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PromptSchema(Schema):
    id = fields.Int(dump_only = True)
    project_id = fields.Int(required=True)
    name = fields.Str(required=True)


class VersionSchema(Schema):
    id = fields. Int(dump_only = True)
    prompt_id = fields.Int(required = True)
    prompt_text =fields.Str(required= True)    


