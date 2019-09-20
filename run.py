#!/usr/bin/python
# -*- coding: utf-8 -*-
# run.py
import os
from pgs_api import app
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler
import struct
import socket

"""
PGS API is a boilerplate application that allows you to create Python + Flask API
applications based on a Model-View-Controller (MVC) pattern. It supports out of the
box interaction with Mongo DB Document Database, JWT Token Generation and Authentication,
basic and extensible identity model.
"""

__author__ = "Alejandro Toba (alejandro.toba@gmail.com)"
__version__ = "1.0"

KEY_SSL = "key.pem"
CERT_SSL = "cert.pem"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    #app.run('0.0.0.0', port)
    host_name = socket.gethostname()
    #print(host_name)
    
    if host_name == 'BEELZEBUB':
        app.run('0.0.0.0', port)
    app.run(port = port, host='0.0.0.0', debug=True, use_reloader=True, ssl_context=(CERT_SSL,KEY_SSL))

