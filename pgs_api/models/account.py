#!/usr/bin/python
# -*- coding: utf-8 -*-
from mongoengine import Document, StringField, DateTimeField, IntField, FloatField, EmbeddedDocumentListField, BooleanField, ListField, EmbeddedDocumentField
from werkzeug.security import safe_str_cmp
from flask import jsonify
from pgs_api.security.entropy import gen_salt, compute_hash
import datetime
from pgs_api.models.plan import Plan, PlanService


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
    def __init__(self, user_id, username, name, last_name, email, gender, age, country_id, smoker, 
    user_type, spouse_age, spouse_gender, dependents, maternity, transplant): 
        self.id = user_id
        self.user_id = user_id
        self.username = username
        self.name = name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.age = age
        self.country_id = country_id
        self.smoker = smoker
        self.user_type = user_type
        self.spouse_age = spouse_age
        self.spouse_gender = spouse_gender
        self.dependents = dependents
        self.maternity = maternity
        self.transplant = transplant

    # --------------------------------------------------------------------------
    # METHOD STR
    # --------------------------------------------------------------------------
    def as_json(self):
        """The method return as json."""
        return jsonify({
            "user_id": self.user_id,
            "username": self.username,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "gender": self.gender,
            "age": self.age,
            "country_id": self.country_id,
            "smoker": self.smoker,
            "user_type": self.user_type,
            "spouse_age": self.spouse_age,
            "spouse_gender": self.spouse_gender,
            "dependents": self.dependents,
            "maternity": self.maternity,
            "transplant": self.transplant
            
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

    last_name = StringField(max_length=120, required=False, default = '')

    email = StringField(max_length=120, required=True, unique=True)

    username = StringField(max_length=120, required=False, unique=True)

    gender = StringField(max_length=40, required=True)

    #dob = DateTimeField(max_length=120, required=False)

    age = IntField(max_length=2, required=True, default = 18)

    country_id = StringField(max_length=40, required=True)

    smoker = BooleanField(max_length=10, required=False)

    maternity = BooleanField(max_length=10, required=False)

    transplant = BooleanField(max_length=10, required=False)

    #surgical = StringField(max_length=40, required=False)

    #health = StringField(max_length=120, required=False)

    dependents = IntField(max_length=2, required=False, default = 0)

    spouse_age = IntField(max_length=2, required=False, default = 0)

    spouse_gender = StringField(max_length=40, required=False, default = 'none')

    user_type = IntField(max_length=2, required=True, default=4)

    password = StringField(max_length=256, required=False)

    salt = StringField(max_length=17, required=True, default=gen_salt(17))

    plan_id = StringField(max_length=40, required=False)

    #plans = ListField(EmbeddedDocumentField('Plan'))

    price = FloatField(max_length=120, required=False)

    date_modified = DateTimeField(default=datetime.datetime.now)

    meta = {
        'indexes': [
            'user_id',
            'username',
            'email',
             {'fields': ['$email', "$name", "$last_name"],}
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
    # METHOD UPDATE USER
    # --------------------------------------------------------------------------
    def update_user(self, data):
        """The method for update user"""
        #self.id = user_id
        #self.user_id = user_id
        self.username = data['email']
        self.name = data['name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.gender = data['gender']
        self.age = data['age']
        self.country_id = data['country_id']
        self.smoker = data['smoker']
        #self.surgical = data['surgical']
        #self.health = health
        #self.user_type = user_type
        self.spouse_age = data['spouse_age']
        self.spouse_gender = data['spouse_gender']
        self.dependents = data['dependents']
        self.maternity = data['maternity']
        self.transplant = data['transplant']
        self.save()
        return True


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
    # METHOD UPDATE QUESTION SURGICAL
    # --------------------------------------------------------------------------
    # def update_surgical(self, data):
    #     """The method for update surgical"""
    #     self.surgical = data
    #     self.save()
    #     return True

    # --------------------------------------------------------------------------
    # METHOD UPDATE QUESTION HEALTH
    # --------------------------------------------------------------------------
    # def update_health(self, data):
    #     """The method for update health"""
    #     self.health = data
    #     self.save()
    #     return True

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
                               self.email, 
                               self.gender,
                               self.age,
                               self.country_id,
                               self.smoker, 
                               self.user_type, 
                               self.spouse_age,
                               self.spouse_gender, 
                               self.dependents, 
                               self.maternity, 
                               self.transplant)
   
    # --------------------------------------------------------------------------
    # METHOD update plan user
    # --------------------------------------------------------------------------
    def update_plan(self, plan_id):
        """The method for update health"""
        self.plan_id = plan_id
        self.save()
        return True

    # --------------------------------------------------------------------------
    # METHOD update plan user
    # --------------------------------------------------------------------------
    def update_price(self, price):
        """The method for update health"""
        self.price = price
        self.save()
        return True


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

    def delete_user(self):
        """The method for delete """
        user = User.objects.get(user_id=self.user_id).delete()
        return True


