from pgs_api import app
from flask import request, jsonify
from pgs_api.models.plan import Plan
from pgs_api.models.plan import PlanService
from pgs_api.models.country import Country, CountryService
from pgs_api.extensions.jsonp import enable_jsonp
from pgs_api.extensions.error_handling import ErrorResponse
from pgs_api.extensions.error_handling import SuccessResponse
from flask_jwt import jwt_required, current_identity
import uuid
import mongoengine
import re
import pymongo

# --------------------------------------------------------------------------
# GET: /country/<uid>
# --------------------------------------------------------------------------
@app.route('/api/v1/country/<country_id>', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_country_by_id(country_id):
    try:
        service = CountryService(country_id)
        data = service.get_country()
        if data:
            return jsonify(data)
        return ErrorResponse('Plan not found', 'The provided country_id is not valid').as_json()
    except:
        app.logger.error('Invalid json received for plan: %s', country_id)
        return ErrorResponse('Could not get', 'Invalid data provided').as_json()

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
# PUT: /company/<uid>/status
# --------------------------------------------------------------------------
@app.route('/api/v1/country/<country_id>/status', methods=['PUT'])
#@jwt_required()
@enable_jsonp
def update_country_status(country_id):
    try:
        service = CountryService(country_id)
        plan = service.get_country()
        if plan.update_status():
            app.logger.info('Updated status for country_id: %s', country_id)
            return SuccessResponse('Success', 'Status updated successfully', 'STATUS_OK').as_json()
    except:
        app.logger.error('Invalid json received for country: %s', country_id)
        return ErrorResponse('Could not update status', 'Invalid status provided').as_json()

# --------------------------------------------------------------------------
# GET: /country/countries
# --------------------------------------------------------------------------
@app.route('/api/v1/country/countries/', defaults={'term':''}, methods=['GET'])
@app.route('/api/v1/country/countries/<term>', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_all_countries(term):
    service = CountryService
    data = service.get_countries(term)
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