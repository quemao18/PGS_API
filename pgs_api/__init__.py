#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt import JWT
from flask_cors import CORS

# ------------------------------------------------------------------------------
# SETUP GENERAL APPLICATION
# ------------------------------------------------------------------------------

__version__ = '1.0'
app = Flask('pgs_api')
CORS(app)

app.config.from_object('config')
app.debug = False


# ------------------------------------------------------------------------------
# SETUP LOGGING
# ------------------------------------------------------------------------------

handler = RotatingFileHandler('pgs_api.log', maxBytes=1000000, backupCount=5)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# ------------------------------------------------------------------------------
# SETUP MONGO DB 
# ------------------------------------------------------------------------------

db = MongoEngine(app)

# ------------------------------------------------------------------------------
# SETUP JWT AUTHENTICATION
# ------------------------------------------------------------------------------

# Import all pgs_api controller files
from pgs_api.controllers import *
from pgs_api.security import idam

jwt = JWT(app, idam.authenticate, idam.identity)
