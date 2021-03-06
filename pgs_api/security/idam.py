#!/usr/bin/python
# -*- coding: utf-8 -*-
from pgs_api import app
from pgs_api.models.account import User
from mongoengine import *
import json

# ------------------------------------------------------------------------------
# IDENTITY AND ACCESS MANAGEMENT MODULE
# ------------------------------------------------------------------------------
# This section provides identity and access management functions and class
# definitions.


# ------------------------------------------------------------------------------
# FUNCTION AUTHENTICATE
# ------------------------------------------------------------------------------
# Checks given credential in order to authenticate or deny authentication to the
# API.
def authenticate(username, password):
    try:
        user = User.objects.get(username=username)
        if user and user.authenticate(password=password):
            app.logger.warning('Authenticated user with correct credentials user: '+username)
            return user.get_identity()
        else:
            app.logger.warning('User: attempted to login using invalid credentials. ' + username)
    except DoesNotExist:
        app.logger.warning('A logging attempt of non-existing user: occurred. ' + username)
    except MultipleObjectsReturned:
        app.logger.error('The username has more than 1 match in database. Urgent revision required. '+username)
    return None


# ------------------------------------------------------------------------------
# FUNCTION IDENTITY
# ------------------------------------------------------------------------------
# Gets the User associated with a given identity
def identity(payload):
    try:
        user_id = payload['identity']
        user = User.objects.get(user_id=user_id)
        return user.get_identity()
    except DoesNotExist:
        app.logger.warning('A retrieval attempt of non-existing user occurred: ' + user_id)
    except MultipleObjectsReturned:
        app.logger.error('The username has more than 1 match in database. Urgent revision required. '+user_id)
    return None


# ------------------------------------------------------------------------------
# FIND USER
# ------------------------------------------------------------------------------
def find_user(user_id):
    try:
        user = User.objects.get(user_id=user_id)
        return user.get_identity()
    except DoesNotExist:
        app.logger.warning('A retrieval attempt of non-existing user occurred: ' + user_id)
    except MultipleObjectsReturned:
        app.logger.error('The username has more than 1 match in database. Urgent revision required. ' + user_id)
    return None

# ------------------------------------------------------------------------------
# FIND USER EMAIL
# ------------------------------------------------------------------------------
def find_user_email(email):
    try:
        user = User.objects.fields(slice__plans=-10).get(email=email)
        return user.get_identity()
    except DoesNotExist:
        app.logger.warning('A retrieval attempt of non-existing user occurred: ' + email)
    except MultipleObjectsReturned:
        app.logger.error('The username has more than 1 match in database. Urgent revision required. ' + email)
    return None

# ------------------------------------------------------------------------------
# FIND USERS By EMAIL Logged
# ------------------------------------------------------------------------------
def find_users_email_logged(email):
    try:
        users = User.objects.fields(slice__plans=-10).filter(email_logged=email).order_by('-date_modified').limit(100)
        # print(email)
        return users
    except DoesNotExist:
        app.logger.warning('A retrieval attempt of non-existing user occurred: ' + email)
    # except MultipleObjectsReturned:
    #     app.logger.error('The username has more than 1 match in database. Urgent revision required. ' + email)
    return None

# ------------------------------------------------------------------------------
# ALL USERS
# ------------------------------------------------------------------------------
def all_users(term):
    if term=='':
        users = User.objects.all().order_by('-date_modified')
    else:
        users = User.objects.search_text(term).order_by('-date_modified').limit(100)
    return users