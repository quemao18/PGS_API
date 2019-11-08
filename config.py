import datetime
# Turns on debugging features in Flask
DEBUG = True
#
# For use in web_app emails
MAIL_FROM_EMAIL = "info@gernet-api.org"
#
# This is a secret key that is used by Flask to sign cookies.
# Its also used by extensions like Flask-Bcrypt. You should
# define this in your instance folder to keep it out of version
# control.
SECRET_KEY = 'change_this_please'  # Change for production
#
# Configuration for the Flask-Bcrypt extension
BCRYPT_LEVEL = 12
#
# ----------------------------------------------------------------
# JWT CONFIGURATIONS
# ----------------------------------------------------------------
JWT_AUTH_URL_RULE = '/api/v1/auth'
JWT_EXPIRATION_DELTA = datetime.timedelta(3200) # Set the token validity
#UPLOAD_FOLDER = 'D:\Proyectos\pgs_api\public\img'
#UPLOAD_FOLDER = 'D:\Proyectos\pgs_dashboard\src\\assets\img\logos' #se suben a firebase
#
# ----------------------------------------------------------------
# ----------------------------------------------------------------
# MONGO DATABASE CONFIGURATION
# ----------------------------------------------------------------
# MongoDB configuration parameters
MONGODB_DB = 'pgs'
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017 #port here
MONGODB_USERNAME = ''
MONGODB_PASSWORD = ''

# ------------------------
# SMTP SETTINGS AWS SES
#------------------------

HOST_SMTP = 'email-smtp.us-east-1.amazonaws.com'
FROM_EMAIL = 'info@rodasalias.com'
USER_SMTP = 'AKIA4NXPK3KZCM7RYQHR'
PASS_SMTP = 'BG/ibH6Hb39NVDG9iVja6mR2KWXGFYC0jyziqNXAnKii'
HOST_SMTP = 'smtp.gmail.com'
USER_SMTP = 'alejandro.toba@gmail.com'
PASS_SMTP = 'Astaroth_0455'
PORT_SMTP = 587

