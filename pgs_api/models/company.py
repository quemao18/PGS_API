#!/usr/bin/python
# -*- coding: utf-8 -*-
from mongoengine import Document, StringField, DateTimeField, BooleanField
from werkzeug.security import safe_str_cmp
from flask import jsonify
from pgs_api.security.entropy import gen_salt, compute_hash
import datetime
from pgs_api.models.plan import Plan


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
    def __init__(self, id, company_id, name, logo, description, email): 
        self.id = id
        self.company_id = company_id
        self.logo = logo
        self.email = email
        self.name = name
        self.description = description

        

    # --------------------------------------------------------------------------
    # METHOD STR
    # --------------------------------------------------------------------------
    def as_json(self):
        """The method return as json."""
        return jsonify({
            "id": self.id,
            "company_id": self.company_id,
            "logo": self.logo,
            "email": self.email,
            "name": self.name,
            "description": self.description
        })


# ------------------------------------------------------------------------------
# CLASS USER
# ------------------------------------------------------------------------------
# Represents a User within the Satellite Identity sub-system.
class Company(Document):
    """Class Company."""
    # --------------------------------------------------------------------------
    # COMPANY PROPERTIES
    # --------------------------------------------------------------------------
    
    company_id = StringField(max_length=40, required=True)

    name = StringField(max_length=120, required=True)

    email = StringField(max_length=120, required=True, unique=True)

    status = BooleanField(max_length=5, required=False)

    logo = StringField(max_length=250, required=False)

    description = StringField(max_length=120, required=False)

    date_modified = DateTimeField(default=datetime.datetime.now)

    meta = {
            'indexes': [
                'company_id',
                'email',
                {'fields': ['$email', "$name"],}
            ]
        }

    # --------------------------------------------------------------------------
    # METHOD STR
    # --------------------------------------------------------------------------
    # Creates a string representation of a user
    def __str__(self):
        return "Company(name='%s')" % self.name

    # --------------------------------------------------------------------------
    # METHOD IS_AUTHORIZED_TO
    # --------------------------------------------------------------------------
    def is_authorized_to(self, action):
        """The method is authorized"""
        return action in self.claims

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
    # METHOD UPDATE LOGO URL
    # --------------------------------------------------------------------------
    def update_logo_url(self, url):
        """The method for update logo url"""
        self.logo = url
        self.save()
        return True

    # --------------------------------------------------------------------------
    # METHOD UPDATE COMPANY
    # --------------------------------------------------------------------------
    def update_company(self, data):
        """The method for update company"""
        self.email = data['email']
        self.name = data['name']
        self.logo = data['logo']
        self.description = data['description']
        self.date_modified = datetime.datetime.now
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
    # METHOD GET IDENTITY
    # --------------------------------------------------------------------------
    def get_identity(self):
        """The method for get identity"""
        return SessionIdentity(self.company_id,
                               self.name,
                               self.email,
                               self.description,
                               self.logo
                              )

# ------------------------------------------------------------------------------
# CLASS USER SERVICE
# ------------------------------------------------------------------------------
# Represents a user service that allows easy management of User objects
# pylint: disable=too-few-public-methods
class CompanyService: 
    """The class company service"""
    def __init__(self, company_id):
        self.company_id = company_id

    def get_company(self):
        """The method for get company"""
        data = Company.objects.get(company_id=self.company_id)
        if data:
            return data
        return None
    
    def get_company_plans(self):
        """The method for get company plans"""
        data = Plan.objects(company_id=self.company_id)
        if data:
            return data
        return None

    def get_plan_name(self):
        """The method for get company name plan"""
        data = Plan.objects(company_id=self.company_id)
        if data:
            return data
        return None

    def get_companies(term):
        """The method for get companies"""
        if term=='':
            data = Company.objects.all()
        else:
            data = Company.objects.search_text(term).limit(100)
        return data


