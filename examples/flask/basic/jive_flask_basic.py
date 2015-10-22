#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, send_from_directory
import logging
import jive_sdk

####################
## CONFIG SECTION ##
####################
clientId = "REPLACE_ME.i"         #"TODO_REPLACE_ME_WITH_YOUR_ADD_ON_INFO"
clientSecret = "REPLACE_ME.s"     #"TODO_REPLACE_ME_WITH_YOUR_ADD_ON_INFO"
PORT = 8090
####################

app = Flask(__name__)

@app.route('/jive/addon/register', methods=['POST'])
def example_register():
    if not request.json:
        abort(400)
    
    if jive_sdk.is_valid_registration_notification(request.json):
        logging.info("Success")
        return "OK",200
            
    logging.error("Unable to register add-on with service")
    
    return "ERROR",401

@app.route('/jive/addon/unregister', methods=['POST'])
def example_unregister():
    if not request.json:
        abort(400)
        
    if jive_sdk.is_valid_registration_notification(request.json, clientSecret=clientSecret):
        logging.info("Success")
        return "OK",200
            
    logging.error("Unable to register add-on with service")
    
    return "ERROR",401

@app.route('/<path:path>', methods=['GET'])

#registering last
#see: http://codepen.io/asommer70/post/serving-a-static-directory-with-flask
@app.route('/<path:path>')
def example_send_static_file(path):
    authorization = request.headers.get('Authorization')
    
    if not (authorization):
        ### TODO: ADDITIONAL LOGIC TO DETERMINE IF REQUEST SHOULD BE HONORED, i.e. images vs. HTML, etc..
        return app.send_static_file(path)
    
    if jivesdk.is_valid_authorization(authorization,clientId,clientSecret):
        logging.info("Success")
        return app.send_static_file(path)
    
    logging.error("Unable to validate signed-fetch headers")
    return "ERROR",401
  

@app.route('/jive/test/signed', methods=['POST'])
def example_signed_fetch():
    authorization = request.headers.get('Authorization')
    
    if jivesdk.is_valid_authorization(authorization,clientId,clientSecret):
        logging.info("Success")
        return "OK",200
            
    logging.error("Unable to validate signed-fetch headers")
    return "ERROR",401

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True)