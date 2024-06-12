from flask import Blueprint, request, jsonify
from yourproject.app.extensions import db
from yourproject.app.models.project import Project
from yourproject.app.models.prompt import Prompt
from yourproject.app.models.version import Version

from yourproject.app.schemas import ProjectSchema
from yourproject.app.schemas import PromptSchema
from yourproject.app.schemas import VersionSchema
from marshmallow import ValidationError

project_blueprint = Blueprint('project', __name__)
project_schema = ProjectSchema()
project_schemas = ProjectSchema(many=True)


#  projects
@project_blueprint.route('/', methods=['POST'])
def add_project():
    data = request.get_json()
    try:
        project = Project.add(data)
        return project_schema.dump(project), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@project_blueprint.route('/', methods=['GET'])
def get_projects():
    projects = Project.get_all()
    return jsonify(project_schemas.dump(projects))


@project_blueprint.route('/<int:id>', methods=['PUT'])
def update_project(id):
    data = request.get_json()
    try:
        project = Project.update_by_id(id, data)
        return project_schema.dump(project)
    except ValidationError as err:
        return jsonify(err.messages), 400

@project_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_project(id):
    Project.delete_by_id(id)
    return jsonify({'message': 'Project deleted successfully'}), 200




#  prompts

@project_blueprint.route('/projects/<int:project_id>/prompts', methods=['POST'])
def add_prompt(project_id):
    data = request.get_json()
    try:
        prompt = Prompt.add(project_id=project_id, name=data['name'])
        return PromptSchema().dump(prompt), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@project_blueprint.route('/prompts/<int:prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
    prompt = Prompt.get(prompt_id)
    if prompt:
        return PromptSchema().dump(prompt)
    else:
        return jsonify({'message': 'Prompt not found'}), 404

@project_blueprint.route('/prompts/<int:prompt_id>', methods=['PUT'])
def update_prompt(prompt_id):
    prompt = Prompt.get(prompt_id)
    if not prompt:
        return jsonify({'message': 'Prompt not found'}), 404

    data = request.get_json()
    try:
        prompt.update(name=data['name'])
        return PromptSchema().dump(prompt)
    except ValidationError as err:
        return jsonify(err.messages), 400

@project_blueprint.route('/prompts/<int:prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
    prompt = Prompt.get(prompt_id)
    if not prompt:
        return jsonify({'message': 'Prompt not found'}), 404

    prompt.delete()
    return jsonify({'message': 'Prompt deleted successfully'}), 200


#  versions
@project_blueprint.route('/versions', methods=['POST'])
def add_version():
    data = request.get_json()
    version = Version.add(prompt_id=data['prompt_id'], prompt_text=data['prompt_text'])
    return VersionSchema().dump(version), 201

@project_blueprint.route('/versions/<int:version_id>', methods=['GET'])
def get_version(version_id):
    version = Version.get(version_id)
    if version:
        return VersionSchema().dump(version)
    else:
        return jsonify({'message': 'Version not found'}), 404

@project_blueprint.route('/versions/<int:version_id>', methods=['PUT'])
def update_version(version_id):
    data = request.get_json()
    version = Version.get(version_id)
    if version:
        version.update(prompt_text=data['prompt_text'])
        return VersionSchema().dump(version)
    else:
        return jsonify({'message': 'Version not found'}), 404

@project_blueprint.route('/versions/<int:version_id>', methods=['DELETE'])
def delete_version(version_id):
    version = Version.get(version_id)
    if version:
        version.delete()
        return jsonify({'message': 'Version deleted successfully'}), 200
    else:
        return jsonify({'message': 'Version not found'}), 404


