#!/usr/bin/python
# -*- coding: utf-8 -*-
from mongoengine import Document, StringField, DateTimeField
from werkzeug.security import safe_str_cmp
from flask import jsonify
from pgs_api.security.entropy import gen_salt, compute_hash
import datetime


# ------------------------------------------------------------------------------
# CLASS IDENTITY
# ------------------------------------------------------------------------------
# pylint: disable=too-few-public-methods
class SessionIdentity:
    """Class session Identity."""
    # --------------------------------------------------------------------------
    # CONSTRUCTOR METHOD
    # --------------------------------------------------------------------------
    # pylint: disable=too-many-arguments
    def __init__(self, id, username, name, last_name, email): 
        self.id = id
        self.username = username
        self.name = name
        self.last_name = last_name
        self.email = email

    # --------------------------------------------------------------------------
    # METHOD STR
    # --------------------------------------------------------------------------
    def as_json(self):
        """The method return as json."""
        return jsonify({
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email
        })


# ------------------------------------------------------------------------------
# CLASS USER
# ------------------------------------------------------------------------------
# Represents a User within the Satellite Identity sub-system.
class User(Document):
    """Class User."""
    # --------------------------------------------------------------------------
    # USER PROPERTIES
    # --------------------------------------------------------------------------

    user_id = StringField(max_length=40, required=True)

    name = StringField(max_length=120, required=True)

    last_name = StringField(max_length=120, required=True)

    email = StringField(max_length=120, required=True, unique=True)

    username = StringField(max_length=120, required=True, unique=True)

    password = StringField(max_length=256, required=True)

    salt = StringField(max_length=17, required=True, default=gen_salt(17))

    date_modified = DateTimeField(default=datetime.datetime.now)

    meta = {
        'indexes': [
            'user_id',
            'username',
            'email'
        ]
    }

    # --------------------------------------------------------------------------
    # METHOD STR
    # --------------------------------------------------------------------------
    # Creates a string representation of a user
    def __str__(self):
        return "User(username='%s')" % self.username

    # --------------------------------------------------------------------------
    # METHOD IS_AUTHORIZED_TO
    # --------------------------------------------------------------------------
    def is_authorized_to(self, action):
        """The method is authorized"""
        return action in self.claims

    # --------------------------------------------------------------------------
    # METHOD ADD_CLAIM
    # --------------------------------------------------------------------------
    def add_claim(self, claim):
        """The method for add claim"""
        if claim not in self.claims:
            self.claims.append(claim)
            self.save()

    # --------------------------------------------------------------------------
    # METHOD UPDATE PASSWORD
    # --------------------------------------------------------------------------
    def update_password(self, password):
        """The method for update password"""
        self.password = compute_hash(password, self.salt)
        self.save()
        return True

    # --------------------------------------------------------------------------
    # METHOD UPDATE EMAIL
    # --------------------------------------------------------------------------
    def update_email(self, email):
        """The method for update email"""
        self.email = email
        self.save()
        return True

    # --------------------------------------------------------------------------
    # METHOD AUTHENTICATE
    # --------------------------------------------------------------------------
    def authenticate(self, password):
        """The method for authenticate user"""
        challenge = compute_hash(password, self.salt)
        return safe_str_cmp(self.password.encode('utf-8'), challenge.encode('utf-8'))

    # --------------------------------------------------------------------------
    # METHOD GET IDENTITY
    # --------------------------------------------------------------------------
    def get_identity(self):
        """The method for get identity"""
        return SessionIdentity(self.user_id,
                               self.username,
                               self.name,
                               self.last_name,
                               self.email)


# ------------------------------------------------------------------------------
# CLASS USER SERVICE
# ------------------------------------------------------------------------------
# Represents a user service that allows easy management of User objects
# pylint: disable=too-few-public-methods
class UserService: 
    """The class user service"""
    def __init__(self, user_id):
        self.user_id = user_id

    def get_user(self):
        """The method for get user"""
        user = User.objects.get(user_id=self.user_id)
        if user:
            return user
        return None
