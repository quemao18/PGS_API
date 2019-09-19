from pgs_api import app
from flask import request, jsonify
from pgs_api.models.plan import Plan
from pgs_api.models.plan import PlanService
from pgs_api.models.country import Country, CountryService
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
# GET PLAN
# --------------------------------------------------------------------------
# Gets the account information associated with current session in the system
@app.route('/api/v1/plan', methods=['GET'])
# @jwt_required()
@enable_jsonp
def get_plan():
    return current_identity.as_json()


# --------------------------------------------------------------------------
# GET: /plan/<uid>
# --------------------------------------------------------------------------
@app.route('/api/v1/plan/<plan_id>', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_plan_by_id(plan_id):
    service = PlanService(plan_id)
    data = service.get_plan()
    if data:
        return jsonify(data)
    return ErrorResponse('Plan not found', 'The provided plan_id is not valid').as_json()


# --------------------------------------------------------------------------
# GET: /plan/plans
# --------------------------------------------------------------------------
@app.route('/api/v1/plan/plans', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_all_plans():
    service = PlanService
    data = service.get_plans()
    if data: 
        return jsonify(data) 
    return ErrorResponse('Companies not found', 'Companies collections is empty').as_json()

# --------------------------------------------------------------------------
# PUT: /company/<uid>/status
# --------------------------------------------------------------------------
@app.route('/api/v1/plan/<plan_id>/status', methods=['PUT'])
#@jwt_required()
@enable_jsonp
def update_plan_status(plan_id):
    try:
        service = PlanService(plan_id)
        plan = service.get_plan()
        if plan.update_status():
            app.logger.info('Updated status for plan_id: %s', plan_id)
            return SuccessResponse('Success', 'Status updated successfully', 'STATUS_OK').as_json()
    except:
        app.logger.error('Invalid json received for company: %s', plan_id)
        return ErrorResponse('Could not update status', 'Invalid status provided').as_json()

# --------------------------------------------------------------------------
# PUT: /plan/<uid>
# --------------------------------------------------------------------------
@app.route('/api/v1/plan/<plan_id>', methods=['PUT'])
@jwt_required()
@enable_jsonp
def put_plan(plan_id):
    try:
        data = request.get_json()
        app.logger.info('Updated plan_id: %s', data)
        #data = json.loads(request.data, strict=False)
        service = PlanService(plan_id)
        plan = service.get_plan()
        if plan.update_plan(data):
            app.logger.info('Updated plan_id: %s', plan_id)
            return SuccessResponse('Success', 'Updated successfully', 'UPDATE_OK').as_json()
    except:
        app.logger.error('Invalid json received for plan: %s', plan_id)
        return ErrorResponse('Could not update', 'Invalid data provided').as_json()


# --------------------------------------------------------------------------
# POST: /plan
# --------------------------------------------------------------------------
# Registers a new plan in the system using pgs_api Identity Sub-System
@app.route('/api/v1/plan', methods=['POST'])
@jwt_required()
@enable_jsonp
def post_plan():
    data = request.get_json()
    service = CompanyService(data['company_id'])
    exist = service.get_company_plans()
    con = True
    if exist:
        for x in exist:
            if x.name == data['name']:
                con = False
    if data and con:
        try:
            res = Plan(
            plan_id=str(uuid.uuid4()),
            company_id = data['company_id'],
            name=data['name'],
            price=data['price'],
            description=data['description']
            )
            res.save(validate=False)
            app.logger.info('Plan %s was created', res.plan_id)
            return SuccessResponse(res.plan_id, 'Plan created successfully', 'n/a').as_json()
        except mongoengine.errors.NotUniqueError as e:
            found = re.search('"(.+?)"', str(e)).group(1)
            if found == res.name:
                return ErrorResponse('Name is registred ', str(e)).as_json()
    if con==False:
         return ErrorResponse('Name exist', 'Name of plan exist for company ').as_json()
    return ErrorResponse('Error processing request', 'The provided data is not valid').as_json()

# --------------------------------------------------------------------------
# DELETE: /plan/<uid>
# --------------------------------------------------------------------------
@app.route('/api/v1/plan/<plan_id>', methods=['DELETE'])
@jwt_required()
@enable_jsonp
def delete_plan(plan_id):
    try:
        service = PlanService(plan_id)
        x = service.delete()
        if x:
            app.logger.info('Delete plan_id: %s', plan_id)
            return SuccessResponse('Success', 'Delete successfully', 'DELETE_OK').as_json()
    except:
        app.logger.error('Invalid json received for company: %s', plan_id)
        return ErrorResponse('Could not delete plan_id', 'Invalid plan_id provided').as_json()


# --------------------------------------------------------------------------
# POST: /country
# --------------------------------------------------------------------------
# Registers a new plan in the system using pgs_api Identity Sub-System
@app.route('/api/v1/country', methods=['POST'])
@jwt_required()
@enable_jsonp
def post_country():
    data = request.get_json()
    if data:
        try:
            res = Country(
            country_id=str(uuid.uuid4()),
            name=data['name'],
            )
            res.save(validate=False)
            app.logger.info('Country %s was created', res.country_id)
            return SuccessResponse(res.country_id, 'Country created successfully', 'n/a').as_json()
        except mongoengine.errors.NotUniqueError as e:
            return ErrorResponse('Name is registred ',data['name']).as_json()
    return ErrorResponse('Error processing request', 'The provided data country is not valid').as_json()

# --------------------------------------------------------------------------
# PUT: /country/<uid>
# --------------------------------------------------------------------------
@app.route('/api/v1/country/<country_id>', methods=['PUT'])
@jwt_required()
@enable_jsonp
def put_country(country_id):
    try:
        data = request.get_json()
        service = CountryService(country_id)
        plan = service.get_country()
        if plan.update_country(data):
            app.logger.info('Updated country_id: %s', country_id)
            return SuccessResponse('Success', 'Updated successfully', 'UPDATE_OK').as_json()
    except:
        app.logger.error('Invalid json received for country: %s', country_id)
        return ErrorResponse('Could not update', 'Invalid data provided').as_json()

# --------------------------------------------------------------------------
# GET: /country/countries
# --------------------------------------------------------------------------
@app.route('/api/v1/country/countries', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_all_countries():
    service = CountryService
    data = service.get_countries()
    if data: 
        return jsonify(data) 
    return ErrorResponse('Countries not found', 'Countries collections is empty').as_json()

# --------------------------------------------------------------------------
# DELETE: /country/<uid>
# --------------------------------------------------------------------------
@app.route('/api/v1/country/<country_id>', methods=['DELETE'])
@jwt_required()
@enable_jsonp
def delete_country(country_id):
    try:
        service = CountryService(country_id)
        x = service.delete()
        if x:
            app.logger.info('Delete country_id: %s', country_id)
            return SuccessResponse('Success', 'Delete successfully', 'DELETE_OK').as_json()
    except:
        app.logger.error('Invalid json received for company: %s', country_id)
        return ErrorResponse('Could not delete country_id', 'Invalid country_id provided').as_json()