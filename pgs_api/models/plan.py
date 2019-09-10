#!/usr/bin/python
# -*- coding: utf-8 -*-
from mongoengine import Document, StringField, DateTimeField, FloatField, ListField
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
    def __init__(self, id, company_id, name, plan_id, description, price): 
        self.id = id
        self.plan_id
        self.company_id = company_id
        self.price = price
        self.name = name
        self.description = description

        

    # --------------------------------------------------------------------------
    # METHOD STR
    # --------------------------------------------------------------------------
    def as_json(self):
        """The method return as json."""
        return jsonify({
            "id": self.id,
            "plan_id": self.plan_id,
            "company_id": self.company_id,
            "name": self.name,
            "description": self.description
        })


# ------------------------------------------------------------------------------
# CLASS USER
# ------------------------------------------------------------------------------
# Represents a User within the Satellite Identity sub-system.
class Plan(Document):
    """Class Plan."""
    # --------------------------------------------------------------------------
    # Plan PROPERTIES
    # --------------------------------------------------------------------------
    
    plan_id = StringField(max_length=40, required=True)

    company_id = StringField(max_length=40, required=True)

    name = StringField(max_length=120, required=True)

    price = ListField(max_length=120, required=True)

    description = StringField(max_length=120, required=False)

    date_modified = DateTimeField(default=datetime.datetime.now)

    meta = {
            'indexes': [
                'plan_id',
                'company_id'
            ]
        }

    # --------------------------------------------------------------------------
    # METHOD STR
    # --------------------------------------------------------------------------
    # Creates a string representation of a user
    def __str__(self):
        return "Plan(name='%s')" % self.name

    # --------------------------------------------------------------------------
    # METHOD IS_AUTHORIZED_TO
    # --------------------------------------------------------------------------
    def is_authorized_to(self, action):
        """The method is authorized"""
        return action in self.claims

    # --------------------------------------------------------------------------
    # METHOD UPDATE PASSWORD
    # --------------------------------------------------------------------------
    def update_price(self, price):
        """The method for update price"""
        self.price = price
        self.save()
        return True


    # --------------------------------------------------------------------------
    # METHOD GET IDENTITY
    # --------------------------------------------------------------------------
    def get_identity(self):
        """The method for get identity"""
        return SessionIdentity(self.company_id,
                               self.plan_id,
                               self.name,
                               self.description,
                               self.price
                              )

# ------------------------------------------------------------------------------
# CLASS PLAN SERVICE
# ------------------------------------------------------------------------------
# Represents a user service that allows easy management of User objects
# pylint: disable=too-few-public-methods
class PlanService: 
    """The class company service"""
    def __init__(self, plan_id):
        self.plan_id = plan_id

    def get_plan(self):
        """The method for get plan"""
        data = Plan.objects.get(plan_id=self.plan_id)
        if data:
            return data
        return None

    def get_plans():
        """The method for get companies"""
        data = Plan.objects.all()
        if data:
            return data
        return None


