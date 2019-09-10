from pgs_api import app
from flask import request, jsonify
from pgs_api.models.plan import Plan
from pgs_api.models.plan import PlanService
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
# POST: /plan
# --------------------------------------------------------------------------
# Registers a new user in the system using pgs_api Identity Sub-System
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