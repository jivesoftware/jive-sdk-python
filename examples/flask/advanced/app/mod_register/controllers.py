# Import flask dependencies
from flask import request, abort
import jive_sdk
import logging

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_register = Blueprint('register', __name__, url_prefix='/jive')

# Set the route and accepted methods

@mod_register.route('/addon/register', methods=['POST'])
def addon_register():
    if not request.json:
        abort(400)
    
    if jive_sdk.is_valid_registration_notification(request.json):
        logging.info("Success")
        
        ## TODO: CONNECT YOUR LOGIC
                
        return "OK",200
            
    logging.error("Unable to register add-on with service")
    
    return "ERROR",401

@mod_register.route('/addon/unregister', methods=['POST'])
def addon_unregister():
    if not request.json:
        abort(400)
    
    if jive_sdk.is_valid_registration_notification(request.json, clientSecret=clientSecret):
        logging.info("Success")
        
        ## TODO: CONNECT YOUR LOGIC
        
        return "OK",200
            
    logging.error("Unable to unregister add-on with service")
    
    return "ERROR",401

@mod_register.route('/tile/register', methods=['POST'])
def tile_register():
    if not request.json:
        abort(400)
    
    if jive_sdk.is_valid_registration_notification(request.json):
        logging.info("Success")
        
        ## TODO: CONNECT YOUR LOGIC
        
        return "OK",200
            
    logging.error("Unable to register tile with service")
    
    return "ERROR",401

@mod_register.route('/tile/unregister', methods=['POST'])
def tile_unregister():
    if not request.json:
        abort(400)
    
    if jive_sdk.is_valid_registration_notification(request.json):
        logging.info("Success")
        
        ## TODO: CONNECT YOUR LOGIC
        
        return "OK",200
            
    logging.error("Unable to unregister tile with service")
    
    return "ERROR",401