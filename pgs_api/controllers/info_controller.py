from pgs_api import app
from flask import jsonify


# --------------------------------------------------------------------------
# ROOT RESOURCE OF THE API
# --------------------------------------------------------------------------
#
@app.route('/api/v1/', methods=['GET'])
def get_info():
    return jsonify({
        "platform": "PSG API 1.0",
        "version": "1.0",
        "message": "API para el cotizador de PSG Consulting!",
        "appName": 'PGS Health',
        "email": 'servicioalcliente@pgs-consulting.com',
        "phone1": '+584245881728',
        "phone2": '+17863023698',
    })


# --------------------------------------------------------------------------
# ROOT RESOURCE OF THE IMAGES
# --------------------------------------------------------------------------
#
@app.route('/api/v1/imagesbg', methods=['GET'])
def get_imagesbg():
    return jsonify(
    [
    'https://firebasestorage.googleapis.com/v0/b/pgs-consulting.appspot.com/o/pgs_assets%2Fimages%2Fscreen1.png?alt=media&token=7e207097-6292-434a-bdd4-336c5ac5e88f',
    'https://firebasestorage.googleapis.com/v0/b/pgs-consulting.appspot.com/o/pgs_assets%2Fimages%2Fscreen2.png?alt=media&token=507976f1-f48f-40ce-ab9d-bb0c933ab908',
    'https://firebasestorage.googleapis.com/v0/b/pgs-consulting.appspot.com/o/pgs_assets%2Fimages%2Fscreen3.png?alt=media&token=7bb9ab03-cee0-4126-a4da-03990b6c8819',
    'https://firebasestorage.googleapis.com/v0/b/pgs-consulting.appspot.com/o/pgs_assets%2Fimages%2Fscreen4.png?alt=media&token=edf4579e-50f6-4a01-bebd-69128740be0c',
    'https://firebasestorage.googleapis.com/v0/b/pgs-consulting.appspot.com/o/pgs_assets%2Fimages%2Fscreen5.png?alt=media&token=c31b40aa-9edf-4296-8fed-0663127bbf2c'
    ]
    )

# --------------------------------------------------------------------------
# ROOT RESOURCE OF THE TEXT
# --------------------------------------------------------------------------
#
@app.route('/api/v1/texts', methods=['GET'])
def get_texts():
    return jsonify(
    [
    'No te ofrecemos una póliza, te damos razones para tenerla.',
    'El seguro no es un derecho, es un privilegio.',
    'Tu salud, tu vida y tu familia nos Importan.',
    'Imprescindible en tu camino es contar con nuestro respaldo.'
     ]
    )
    
    