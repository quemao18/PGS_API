#!/usr/bin/python
# -*- coding: utf-8 -*-
from mongoengine import Document, StringField, DateTimeField, FloatField, ListField, BooleanField
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
    def __init__(self, name, country_id): 
        self.id = id
        self.country_id
        self.name = name

    # --------------------------------------------------------------------------
    # METHOD STR
    # --------------------------------------------------------------------------
    def as_json(self):
        """The method return as json."""
        return jsonify({
            "id": self.id,
            "country_id": self.plan_id,
            "name": self.name,
        })


# ------------------------------------------------------------------------------
# CLASS USER
# ------------------------------------------------------------------------------
# Represents a User within the Satellite Identity sub-system.
class Country(Document):
    """Class Plan."""
    # --------------------------------------------------------------------------
    # Plan PROPERTIES
    # --------------------------------------------------------------------------
    
    country_id = StringField(max_length=40, required=True)

    name = StringField(max_length=120, required=True, unique=True)

    status = BooleanField(max_length=5, required=False, default=True)

    date_modified = DateTimeField(default=datetime.datetime.now)

    meta = {
            'indexes': [
                'country_id',
                 {'fields': ["$name"],}
            ]
        }

    # --------------------------------------------------------------------------
    # METHOD STR
    # --------------------------------------------------------------------------
    # Creates a string representation of a user
    def __str__(self):
        return "Country(name='%s')" % self.name

    # --------------------------------------------------------------------------
    # METHOD IS_AUTHORIZED_TO
    # --------------------------------------------------------------------------
    def is_authorized_to(self, action):
        """The method is authorized"""
        return action in self.claims

    # --------------------------------------------------------------------------
    # METHOD UPDATE PLAN
    # --------------------------------------------------------------------------
    def update_country(self, data):
        """The method for update plan"""
        self.name = data['name']
        self.date_modified = datetime.datetime.now
        self.save()
        return True

    # --------------------------------------------------------------------------
    # METHOD UPDATE STATUS
    # --------------------------------------------------------------------------
    def update_status(self):
        """The method for update status"""
        if self.status:
            new_status = False
        else:
            new_status = True
        self.status = new_status
        self.save()
        return True

    # --------------------------------------------------------------------------
    # METHOD GET IDENTITY
    # --------------------------------------------------------------------------
    def get_identity(self):
        """The method for get identity"""
        return SessionIdentity(self.country_id,
                               self.name,
                              )

# ------------------------------------------------------------------------------
# CLASS PLAN SERVICE
# ------------------------------------------------------------------------------
# Represents a user service that allows easy management of User objects
# pylint: disable=too-few-public-methods
class CountryService: 
    """The class plan service"""
    def __init__(self, country_id):
        self.country_id = country_id

    def get_country(self):
        """The method for get plan"""
        data = Country.objects.get(country_id=self.country_id)
        if data:
            return data
        return None

    def get_countries(term):
        """The method for get companies"""
        if term=='':
            data = Country.objects.all().order_by('name')
        else:
            data = Country.objects.search_text(term).order_by('name').limit(100)
        return data

    def delete(self):
        """The method for delete """
        plan = Country.objects.get(country_id=self.country_id).delete()
        return True


