from functools import wraps
import secrets
from flask import request, json, jsonify
import decimal
from app.models import User

def token_required(flask_function):
    @wraps(flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split()
            
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]

        if not token:
            return jsonify({'message': 'Token is not here'}), 401

        try:
            current_user_token = User.query.filter_by(token=token).first()
            print(token)
        except Exception as e:
            print(f"Error during token validation: {e}")
            return jsonify({'message': 'Error during token validation'}), 401

        owner = User.query.filter_by(token=token).first()
        if token != owner.token and secrets.compare_digest(token, owner.token):
            return jsonify({'message': 'The token is invalid'})

        return flask_function(current_user_token, *args, **kwargs)

    return decorated


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)
