#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import logging
import jive_sdk

####################
## CONFIG SECTION ##
####################
clientId = "2xu5an46ry584mvl4id3uq81l4dtxe94.i"         #"TODO_REPLACE_ME_WITH_YOUR_ADD_ON_INFO"
clientSecret = "mq85glgl635zybwem8cfalxj5dw6x7kz.s"     #"TODO_REPLACE_ME_WITH_YOUR_ADD_ON_INFO"
PORT = 8090
####################

app = Flask(__name__)

@app.route('/jive/oauth/register', methods=['POST'])
def test_register():
    if not request.json:
        abort(400)
    
    if jive_sdk.is_valid_registration_notification(request.json):
        logging.info("Success")
        return "OK",200
            
    logging.error("Unable to register add-on with service")
    
    return "ERROR",401

@app.route('/jive/oauth/unregister', methods=['POST'])
def test_unregister():
    if not request.json:
        abort(400)
    
    # REMOVING SUFFIX FOR PROPER BASE64 DECODE
    if clientSecret.endswith(".s"):
        clientSecret = clientSecret[:-2]
        
    if jive_sdk.is_valid_registration_notification(request.json, clientSecret=clientSecret):
        logging.info("Success")
        return "OK",200
            
    logging.error("Unable to register add-on with service")
    
    return "ERROR",401

@app.route('/test', methods=['POST'])
def test_signed_fetch():
    authorization = request.headers.get('Authorization')
    
    if jivesdk.is_valid_authorization(authorization,clientId,clientSecret):
        logging.info("Success")
        return "OK",200
            
    logging.error("Unable to validate signed-fetch headers")
    return "ERROR",401

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True)