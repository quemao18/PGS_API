from pgs_api import app
from flask import request, jsonify, render_template
from pgs_api.models.account import User
from pgs_api.models.account import UserService
from pgs_api.security.idam import find_user, all_users, find_user_email, find_users_email_logged
from pgs_api.extensions.jsonp import enable_jsonp
from pgs_api.extensions.error_handling import ErrorResponse
from pgs_api.extensions.error_handling import SuccessResponse
from flask_jwt import jwt_required, current_identity
import uuid
import mongoengine
import re
import pymongo
from pgs_api.models.plan import Plan

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import FROM_EMAIL, HOST_SMTP, USER_SMTP, PASS_SMTP, PORT_SMTP
import codecs

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
# GET: /account/<email>
# --------------------------------------------------------------------------
@app.route('/api/v1/account/<email>/email', methods=['GET'])
# @jwt_required()
@enable_jsonp
def get_account_by_email(email):
    identity = find_user_email(email)
    # print(identity.as_json())
    if identity:
        return identity.as_json()
    return ErrorResponse('User not found', 'The provided user_id is not valid').as_json()

# --------------------------------------------------------------------------
# GET: /account/<email>/email_logged
# --------------------------------------------------------------------------
@app.route('/api/v1/account/<email>/email_logged', methods=['GET'])
# @jwt_required()
@enable_jsonp
def get_accounts_by_email_logged(email):
    identity = find_users_email_logged(email)
    # print(identity.as_json())
    if identity:
        return jsonify(identity)
    return ErrorResponse('User not found', 'The provided email is not valid').as_json()


# --------------------------------------------------------------------------
# GET: /account/<uid>/plans
# --------------------------------------------------------------------------
@app.route('/api/v1/account/<user_id>/plans', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_plans_by_user_id(user_id):
    user_service = UserService(user_id)
    usr = user_service.get_user()
    plans = Plan.objects(__raw__={'price.country_id': usr.country_id})
    #app.logger.info('Indentity: %s', plans.count())
    if plans:
        return jsonify(plans)
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
# @app.route('/api/v1/account/<user_id>/fields', methods=['PUT'])
# #@jwt_required()
# @enable_jsonp
# def update_account_fields(user_id):
#     try:
#         fields = request.get_json()
#         user_service = UserService(user_id)
#         user = user_service.get_user()
#         if user.update_surgical(fields['surgical']) and user.update_health(fields['health']):
#             app.logger.info('Updated fields for user_id: %s', user_id)
#             return SuccessResponse('Success', 'Question update success', 'FIELDS_OK').as_json()
#     except:
#         app.logger.error('Invalid json received for user: %s', user_id)
#         return ErrorResponse('Could not update fields', 'Invalid data provided').as_json()

# --------------------------------------------------------------------------
# PUT: /account/<uid>/plans
# --------------------------------------------------------------------------
@app.route('/api/v1/account/<user_id>/plans', methods=['POST'])
#@jwt_required()
@enable_jsonp
def update_account_plans(user_id):
    try:
        plans = request.get_json()
        user_service = UserService(user_id)
        user = user_service.get_user()
        if user.update_plans(plans):
            send_email_user(user.user_id, plans)
            app.logger.info('Updated plans for user_id: %s', user_id)
            return SuccessResponse('Success', 'Plans update success', 'PLANS_OK').as_json()
    except:
        app.logger.error('Invalid json received for user: %s', user_id)
        return ErrorResponse('Could not update plans', 'Invalid data provided').as_json()

# --------------------------------------------------------------------------
# POST: /account
# --------------------------------------------------------------------------
# Registers a new user in the system using pgs_api Identity Sub-System
@app.route('/api/v1/account', methods=['POST'])
@enable_jsonp
def post_account():
    user_data = request.get_json()
    app.logger.info('User data %s ', user_data)
    if user_data:
        try:
            user = User(
            user_id=str(uuid.uuid4()),
            name=user_data['name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            username=user_data['username'],
            gender=user_data['gender'],
            age=user_data['age'],
            country_id=user_data['country_id'],
            smoker=user_data['smoker'],
            maternity=user_data['maternity'],
            transplant=user_data['transplant'],
            photo=user_data['photo'],
            password=None, 
            user_type=user_data['user_type'],
            spouse_age=user_data['spouse_age'],
            spouse_gender = user_data['spouse_gender'],
            dependents = user_data['dependents'],
            dependents_ages = user_data['dependents_ages'],
            email_logged = user_data['email_logged'],
            name_logged = user_data['name_logged'],
            photo_logged = user_data['photo_logged']
            )
            user.update_password(user_data['password'])
            user.save(validate=False)
            app.logger.info('User %s was created', user.user_id)
            return SuccessResponse(user.user_id, 'User created successfully', 'n/a').as_json()
        except mongoengine.errors.NotUniqueError as e:
            user = User.objects.get(email=user_data['email'])
            app.logger.info('User %s was updated', user)
            user_service = UserService(user.user_id)
            user = user_service.get_user()
            user.update_user(user_data)
            return SuccessResponse(user.user_id, 'User updated successfully', 'n/a').as_json()
            # found = re.search('"(.+?)"', str(e)).group(1)
            # if found == user.username:
            #     return ErrorResponse('Username is registred ', str(e)).as_json()
            # if found == user.email:
            #     return ErrorResponse('Email is registred ', str(e)).as_json()
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


# --------------------------------------------------------------------------
# SEND MAIL: 
# --------------------------------------------------------------------------
# @app.route('/api/v1/account/<user_id>/send_email', methods=['POST'])

def send_email_user(user_id, plans):
    try:
        # print(plans)
        service = UserService(user_id)
        user = service.get_user()
        app.logger.info('Send email to: %s', user.email)
        # app.logger.info('Send to: %s', FROM_EMAIL)
        me = FROM_EMAIL
        you = user.email
        logged = user.email_logged  
        recipients = [you, logged]
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Solicitud recibida."
        msg['From'] = me
        msg['To'] = ", ".join(recipients)

        # Create the body of the message (a plain-text and an HTML version).
        text = "Hola! " + user.name +", \nHemos recibido tu solicitud, pronto te contactaremos.\nGracias por preferirnos."
        html = render_template('email_success.html', name=user.name, email=user.email, userPlans=plans)
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Send the message via local SMTP server.
        # s = smtplib.SMTP('localhost')
        s = smtplib.SMTP(host=HOST_SMTP, port=PORT_SMTP)
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        s.starttls()
        s.login(USER_SMTP, PASS_SMTP)
        s.sendmail(me, recipients, msg.as_string())
        s.quit
    except Exception as e: 
        app.logger.info('%s', e)
        # print(e)
        return ErrorResponse('Could not send mail user_id', 'Invalid user_id provided').as_json()


# --------------------------------------------------------------------------
# GET PLAN STATS
# --------------------------------------------------------------------------
# Gets the account information associated with current session in the system
@app.route('/api/v1/account/stats_plans', methods=['GET'])
# @jwt_required()
# @enable_jsonp
def get_stats_plans():
    pipeline = [
    # Matchn the documents possible
    # { "$match": { "date": { "$gte": startdate } } },
    # Group the documents and "count" via $sum on the values
    # {'$project': {'_id': 0, 'plans': 1 } },

    {'$unwind': "$plans" },
    {'$group': { 
                "_id": {
                    "plan_name": "$plans.plan_name",
                    "company_name": "$plans.company_name"
                },
                'plan_count': { '$sum': 1 } 
                }
    },

    {'$project': { '_id': 0,'fields': "$_id",'plan_count': 1 , }},
    {'$sort': { 'plan_count': -1 } },
    
    ]
    cursor = User.objects.aggregate(*pipeline)
    
    # cursor = User.collections.aggregate(pipeline)
    # results = list(Foo.objects.aggregate(*pipeline))
    return jsonify([doc for doc in cursor])