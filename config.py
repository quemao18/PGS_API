import datetime
# Turns on debugging features in Flask
DEBUG = False
#
# For use in web_app emails
MAIL_FROM_EMAIL = "info@gernet-api.org"
#
# This is a secret key that is used by Flask to sign cookies.
# Its also used by extensions like Flask-Bcrypt. You should
# define this in your instance folder to keep it out of version
# control.
SECRET_KEY = 'pgs consulting api'  # Change for production
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
FROM_EMAIL = 'info@pgs-consulting.com'
USER_SMTP = 'AKIA4NXPK3KZCM7RYQHR'
PASS_SMTP = 'BG/ibH6Hb39NVDG9iVja6mR2KWXGFYC0jyziqNXAnKii'
PORT_SMTP = 587

HOST_SMTP = 'mail.rodasalias.com'
USER_SMTP = 'test@rodasalias.com'
PASS_SMTP = 'test@rodasalias'
# PORT_SMTP = 465

