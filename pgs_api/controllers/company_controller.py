from pgs_api import app
from flask import request, jsonify
from pgs_api.models.company import Company
from pgs_api.models.company import CompanyService
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
@app.route('/api/v1/company', methods=['GET'])
# @jwt_required()
@enable_jsonp
def get_company():
    return current_identity.as_json()


# --------------------------------------------------------------------------
# GET: /company/<uid>
# --------------------------------------------------------------------------
@app.route('/api/v1/company/<company_id>', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_company_by_id(company_id):
    service = CompanyService(company_id)
    user = service.get_company()
    if user:
        return jsonify(user)
    return ErrorResponse('Company not found', 'The provided company_id is not valid').as_json()



# --------------------------------------------------------------------------
# GET: /company/<uid>/plans
# --------------------------------------------------------------------------
@app.route('/api/v1/company/<company_id>/plans', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_company_plans_by_id(company_id):
    service = CompanyService(company_id)
    data = service.get_company_plans()
    if data:
        return jsonify(data)
    return ErrorResponse('Company not found', 'The provided company_id is not valid').as_json()


# --------------------------------------------------------------------------
# GET: /account/users
# --------------------------------------------------------------------------
@app.route('/api/v1/company/companies', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_all_companies():
    service = CompanyService
    users = service.get_companies()
    if users: 
        return jsonify(users) 
    return ErrorResponse('Companies not found', 'Companies collections is empty').as_json()

# --------------------------------------------------------------------------
# PUT: /account/<uid>/email
# --------------------------------------------------------------------------
@app.route('/api/v1/company/<company_id>/email', methods=['PUT'])
@jwt_required()
@enable_jsonp
def update_company_email(company_id):
    try:
        email_data = request.get_json()
        service = CompanyService(company_id)
        user = service.get_company()
        if user.update_email(email_data['email']):
            app.logger.info('Updated email for company_id: %s', company_id)
            return SuccessResponse('Success', 'Email updated successfully', 'EMAIL_OK').as_json()
    except:
        app.logger.error('Invalid json received for user: %s', company_id)
        return ErrorResponse('Could not update email', 'Invalid email provided').as_json()

# --------------------------------------------------------------------------
# POST: /account
# --------------------------------------------------------------------------
# Registers a new user in the system using pgs_api Identity Sub-System
@app.route('/api/v1/company', methods=['POST'])
@jwt_required()
@enable_jsonp
def post_company():
    user_data = request.get_json()
    if user_data:
        try:
            user = Company(
            company_id=str(uuid.uuid4()),
            name=user_data['name'],
            email=user_data['email'],
            logo=user_data['logo'],
            description=user_data['description']
            )
            user.save(validate=False)
            app.logger.info('Company %s was created', user.company_id)
            return SuccessResponse(user.company_id, 'Company created successfully', 'n/a').as_json()
        except mongoengine.errors.NotUniqueError as e:
            found = re.search('"(.+?)"', str(e)).group(1)
            if found == user.email:
                return ErrorResponse('Email is registred ', str(e)).as_json()
    return ErrorResponse('Error processing request', 'The provided data is not valid').as_json()