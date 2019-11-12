from pgs_api import app
from flask import jsonify


# --------------------------------------------------------------------------
# ROOT RESOURCE OF THE API
# --------------------------------------------------------------------------
#
@app.route('/api/v1/', methods=['GET'])
def get_api_root():
    return jsonify({
        "platform": "PSG API 1.0",
        "version": "1.0",
        "message": "API para el cotizador de PSG Consulting!"
    })
