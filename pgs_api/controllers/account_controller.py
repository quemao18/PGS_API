from pgs_api import app
from flask import request, jsonify
from pgs_api.models.account import User
from pgs_api.models.account import UserService
from pgs_api.security.idam import find_user, all_users
from pgs_api.extensions.jsonp import enable_jsonp
from pgs_api.extensions.error_handling import ErrorResponse
from pgs_api.extensions.error_handling import SuccessResponse
from flask_jwt import jwt_required, current_identity
import uuid
import mongoengine
import re
import pymongo

# --------------------------------------------------------------------------
# GET ACCOUNT
# --------------------------------------------------------------------------
# Gets the account information associated with current session in the system
@app.route('/api/v1/account', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_account():
    return current_identity.as_json()


# --------------------------------------------------------------------------
# GET: /account/<uid>
# --------------------------------------------------------------------------
@app.route('/api/v1/account/<user_id>', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_account_by_id(user_id):
    identity = find_user(user_id)
    if identity:
        return identity.as_json()
    return ErrorResponse('User not found', 'The provided user_id is not valid').as_json()


# --------------------------------------------------------------------------
# GET: /account/users
# --------------------------------------------------------------------------
@app.route('/api/v1/account/accounts/', defaults={'term':''}, methods=['GET'])
@app.route('/api/v1/account/accounts/<term>', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_all_users(term):
    users = all_users(term)
    if users: 
        return jsonify(users) 
    return ErrorResponse('Users not found', 'Users collections is empty').as_json()

# --------------------------------------------------------------------------
# PUT: /account/<uid>/password
# --------------------------------------------------------------------------
@app.route('/api/v1/account/<user_id>/password', methods=['PUT'])
@jwt_required()
@enable_jsonp
def update_account_password(user_id):
    try:
        pass_data = request.get_json()
        user_service = UserService(user_id)
        usr = user_service.get_user()
        if user_id == current_identity.id:
            if usr.update_password(pass_data['password']):
                app.logger.info('Updated password for user_id: %s', user_id)
                return SuccessResponse('Success', 'Password updated successfully', 'EMAIL_OK').as_json()
        else:
            app.logger.error('Permission violation. User not authorized to update other user\'s password. User performing operation %s', user_id)
            return ErrorResponse('Permission violation', 'This action generated a security alert').as_json()
    except:
        app.logger.error('Invalid json received for user: %s', user_id)
        return ErrorResponse('Could not update password', 'Invalid password provided').as_json()


# --------------------------------------------------------------------------
# PUT: /account/<uid>/email
# --------------------------------------------------------------------------
@app.route('/api/v1/account/<user_id>/email', methods=['PUT'])
@jwt_required()
@enable_jsonp
def update_account_email(user_id):
    try:
        email_data = request.get_json()
        user_service = UserService(user_id)
        user = user_service.get_user()
        if user.update_email(email_data['email']):
            app.logger.info('Updated email for user_id: %s', user_id)
            return SuccessResponse('Success', 'Email updated successfully', 'EMAIL_OK').as_json()
    except:
        app.logger.error('Invalid json received for user: %s', user_id)
        return ErrorResponse('Could not update email', 'Invalid email provided').as_json()


# --------------------------------------------------------------------------
# PUT: /account/<uid>/plan
# --------------------------------------------------------------------------
@app.route('/api/v1/account/<user_id>/plan', methods=['PUT'])
@jwt_required()
@enable_jsonp
def update_account_plan(user_id):
    try:
        data = request.get_json()
        user_service = UserService(user_id)
        user = user_service.get_user()
        if user.update_plan(data['plan_id']) and user.update_price(data['price']):
            app.logger.info('Updated plan for user_id: %s', user_id)
            return SuccessResponse('Success', 'Plan updated successfully', 'PLAN_OK').as_json()
    except:
        app.logger.error('Invalid json received for user: %s', user_id)
        return ErrorResponse('Could not update plan', 'Invalid plan_id provided').as_json()



# --------------------------------------------------------------------------
# PUT: /account/<uid>/fields
# --------------------------------------------------------------------------
@app.route('/api/v1/account/<user_id>/fields', methods=['PUT'])
#@jwt_required()
@enable_jsonp
def update_account_fields(user_id):
    try:
        fields = request.get_json()
        user_service = UserService(user_id)
        user = user_service.get_user()
        if user.update_surgical(fields['surgical']) and user.update_health(fields['health']):
            app.logger.info('Updated fields for user_id: %s', user_id)
            return SuccessResponse('Success', 'Question update success', 'FIELDS_OK').as_json()
    except:
        app.logger.error('Invalid json received for user: %s', user_id)
        return ErrorResponse('Could not update fields', 'Invalid data provided').as_json()


# --------------------------------------------------------------------------
# POST: /account
# --------------------------------------------------------------------------
# Registers a new user in the system using pgs_api Identity Sub-System
@app.route('/api/v1/account', methods=['POST'])
@enable_jsonp
def post_account():
    user_data = request.get_json()
    if user_data:
        try:
            user = User(
            user_id=str(uuid.uuid4()),
            name=user_data['name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            username=user_data['username'],
            gender=user_data['gender'],
            dob=user_data['dob'],
            country=user_data['country'],
            smoker=user_data['smoker'],
            password=None, 
            user_type=user_data['user_type']
            )
            user.update_password(user_data['password'])
            user.save(validate=False)
            app.logger.info('User %s was created', user.user_id)
            return SuccessResponse(user.user_id, 'User created successfully', 'n/a').as_json()
        except mongoengine.errors.NotUniqueError as e:
            found = re.search('"(.+?)"', str(e)).group(1)
            if found == user.username:
                return ErrorResponse('Username is registred ', str(e)).as_json()
            if found == user.email:
                return ErrorResponse('Email is registred ', str(e)).as_json()
    return ErrorResponse('Error processing request', 'The provided data is not valid').as_json()

# --------------------------------------------------------------------------
# DELETE: /account/<uid>/email
# --------------------------------------------------------------------------
@app.route('/api/v1/account/<user_id>', methods=['DELETE'])
@jwt_required()
@enable_jsonp
def delete_account(user_id):
    try:
        service = UserService(user_id)
        x = service.delete_user()
        if x:
            app.logger.info('Delete user_id: %s', user_id)
            return SuccessResponse('Success', 'Delete successfully', 'DELETE_OK').as_json()
    except:
        app.logger.error('Invalid json received for user: %s', user_id)
        return ErrorResponse('Could not delete user_id', 'Invalid user_id provided').as_json()