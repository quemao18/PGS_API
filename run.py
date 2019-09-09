#!/usr/bin/python
# -*- coding: utf-8 -*-
# run.py
import os
from pgs_api import app

"""
PGS API is a boilerplate application that allows you to create Python + Flask API
applications based on a Model-View-Controller (MVC) pattern. It supports out of the
box interaction with Mongo DB Document Database, JWT Token Generation and Authentication,
basic and extensible identity model.
"""

__author__ = "Alejandro Toba (alejandro.toba@gmail.com)"
__version__ = "1.0"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run('127.0.0.1', port)
