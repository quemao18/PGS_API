#!/usr/bin/python
# -*- coding: utf-8 -*-
from mongoengine import Document, StringField, DateTimeField, FloatField, ListField, BooleanField, EmbeddedDocument, DecimalField
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
    def __init__(self, id, company_id, name, plan_id, description, price, transplant, maternity, cost_admin): 
        self.id = id
        self.plan_id
        self.company_id = company_id
        self.price = price
        self.name = name
        self.description = description
        self.transplant
        self.maternity
        self.cost_admin

        
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
            "description": self.description,
            "maternity": self.maternity,
            "transplant": self.transplant,
            "cost_admin": self.cost_admin,
            "price": self.price
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

    transplant = DecimalField(required=False, default=0)

    maternity = DecimalField(required=False, default=0)

    cost_admin = DecimalField(required=False, default=0)

    price = ListField(required=True)

    description = StringField(max_length=120, required=False)

    status = BooleanField(max_length=5, required=False, default=True)

    date_modified = DateTimeField(default=datetime.datetime.now)

    meta = {
            'indexes': [
                'plan_id',
                'company_id',
               
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
    # METHOD UPDATE STATUS
    # --------------------------------------------------------------------------
    def update_status(self):
        """The method for update email"""
        if self.status:
            new_status = False
        else:
            new_status = True
        self.status = new_status
        self.save()
        return True

    # --------------------------------------------------------------------------
    # METHOD UPDATE PLAN
    # --------------------------------------------------------------------------
    def update_plan(self, data):
        """The method for update plan"""
        self.name = data['name']
        self.description = data['description']
        self.maternity = data['maternity']
        self.transplant = data['transplant']
        self.cost_admin = data['cost_admin']
        self.price = data['price']
        self.date_modified = datetime.datetime.now
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
                               self.price,
                               self.transplant,
                               self.maternity,
                               self.cost_admin
                              )

# ------------------------------------------------------------------------------
# CLASS PLAN SERVICE
# ------------------------------------------------------------------------------
# Represents a user service that allows easy management of User objects
# pylint: disable=too-few-public-methods
class PlanService: 
    """The class plan service"""
    def __init__(self, plan_id):
        self.plan_id = plan_id

    def get_plan(self):
        """The method for get plan"""
        data = Plan.objects.get(plan_id=self.plan_id)
        if data:
            return data
        return None

    def get_plans():
        """The method for get plans"""
        data = Plan.objects.all()
        if data:
            return data
        return None

    def delete(self):
        """The method for delete """
        plan = Plan.objects.get(plan_id=self.plan_id).delete()
        return True

    def get_plans_country():
        """The method for get plans"""
        data = Plan.objects.get(country_id= self.country_id)
        if data:
            return data
        return None


