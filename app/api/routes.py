from flask import Blueprint, request, jsonify, render_template
from app.helpers import token_required
from app.models import db, User, Project, project_schema, projects_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_data):
    return {'Test': 'Message!!!!'}

@api.route('/projects', methods=['POST'])
@token_required
def add_project(current_user_token):
    name = request.json['name']
    description = request.json['description']
    lang_to_use = request.json['lang_to_use']
    num_of_lines_allowed = request.json['num_of_lines_allowed']
    user_token = current_user_token.token

    print(f'TEST: {current_user_token.token}')

    project = Project(
        name=name,
        description=description,
        lang_to_use=lang_to_use,
        num_of_lines_allowed=num_of_lines_allowed,
        user_token=user_token
    )

    db.session.add(project)
    db.session.commit()

    response = project_schema.dump(project)
    return jsonify(response)

@api.route('/projects', methods=['GET'])
@token_required
def get_projects(current_user_token):
    projects = Project.query.filter_by(user_token=current_user_token.token).all()
    response = projects_schema.dump(projects)
    return jsonify(response)

@api.route('/projects/<string:id>', methods=['POST', 'PUT'])
@token_required
def update_project(current_user_token, id):
    project = Project.query.get(id)

    # Your existing code to update the project...
    project.name = request.json['name']
    project.description = request.json['description']
    project.lang_to_use = request.json['lang_to_use']
    project.num_of_lines_allowed = request.json['num_of_lines_allowed']
    project.user_token = current_user_token.token

    db.session.commit()
    response = project_schema.dump(project)
    return jsonify(response)

@api.route('/projects/<string:id>', methods=['DELETE'])
@token_required
def delete_project(current_user_token, id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()
    response = project_schema.dump(project)
    return jsonify(response)
