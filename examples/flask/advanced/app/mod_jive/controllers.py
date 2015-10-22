# Import flask dependencies
from flask import request, abort, Blueprint, render_template, current_app
import jive_sdk
import logging
import oauth_util
import json

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_jive = Blueprint('jive', __name__, url_prefix='/jive')

# Set the route and accepted methods

@mod_jive.route('/addon/register', methods=['POST'])
def addon_register():
    if not request.json:
        abort(400)
    
    #### VALIDATE JSON PAYLOAD IS FROM A GENUINE JIVE INSTANCE    
    if jive_sdk.is_valid_registration_notification(request.json):
        logging.info("Successful Add-On Registration")
        
        ## CONNECT YOUR LOGIC TO PERSIST THE PAYLOAD, THIS IS JUST AN EXAMPLE
        current_app.config['ADD_ON_REGISTRATION'] = request.json
           
        # RETURN STATUS CODE FOR JIVE TO KNOW IT WAS SUCCESSFUL     
        return "OK",200
            
    logging.error("Unable to register Add-On with service")
    
    # RETURN 40x STATUS CODE TO LET JIVE KNOW IT WAS UNSUCCESSFUL
    return "ERROR",401

@mod_jive.route('/addon/unregister', methods=['POST'])
def addon_unregister():
    if not request.json:
        abort(400)
    
    # CAPTURE THE AUTHORIZATION HEADER
    authorization = request.headers['Authorization']
        
    # PULL THE CLIENT SECRET FROM THE ASSOCIATED ADD-ON, THIS IS JUST AN EXAMPLE    
    if current_app.config['ADD_ON_REGISTRATION']:
        clientId = current_app.config['ADD_ON_REGISTRATION'].get('clientId')
        clientSecret = current_app.config['ADD_ON_REGISTRATION'].get('clientSecret')
    
    if clientSecret:
        # VAIDATE JIVE HEADERS ON THE REQUEST
         if jive_sdk.is_valid_authorization(authorization, clientId, clientSecret):
            logging.info("Successfully Removed Add-On")
            
            ## IMPLEMENT REMOVAL OF ADD_ON FROM PERSISTENCE LAYER, THIS IS AN EXAMPLE
            del current_app.config['ADD_ON_REGISTRATION']
    
            # RETURN STATUS CODE TO INFORM JIVE
            return "OK",200
                
    logging.error("Unable to unregister add-on with service")
            
    # RETURN STATUS CODE TO INFORM JIVE    
    return "ERROR",401

@mod_jive.route('/tile/register', methods=['POST'])
def tile_register():
    if not request.json:
        abort(400)

    authorization = request.headers['Authorization']
    
    addon_registration = current_app.config['ADD_ON_REGISTRATION']
    
    clientId = addon_registration.get('clientId')
    clientSecret = addon_registration.get('clientSecret')
    
    # VALIDATE THAT THE TILE REGISTER REQUEST IS VALID
    if jive_sdk.is_valid_authorization(authorization, clientId, clientSecret):
        logging.info("Successful Tile Registration")
        
        ## PERSIST THE TILE CONFIGURATION TOYOUR LAYER, THIS IS JUST AN EXAMPLE
        current_app.config['TILE_REGISTRATION'] = request.json    
        
        # RETURN STATUS CODE TO INFORM JIVE OF THE SUCCESSFUL REGISTRATION
        return "OK",200
            
    logging.error("Unable to register tile with service")
    
    # RETURN STATUS CODE TO INFORM JIVE OF THE ISSUES
    return "ERROR",401

@mod_jive.route('/tile/unregister', methods=['POST'])
def tile_unregister():
    if not request.json:
        abort(400)
    
    authorization = request.headers['Authorization']
    
    addon_registration = current_app.config['ADD_ON_REGISTRATION']
    
    if not addon_registration: 
        abort(401)
            
    clientId = addon_registration.get('clientId')
    clientSecret = addon_registration.get('clientSecret')
    
    if jive_sdk.is_valid_authorization(authorization, clientId, clientSecret):
        logging.info("Successful Tile Unregistration")
        
        ## TODO: CONNECT YOUR LOGIC
#        del current_app.config['TILE_REGISTRATION']   
        
        return "OK",200
            
    logging.error("Unable to unregister tile with service")
    
    return "ERROR",401

@mod_jive.route('/oauth2/authorize', methods=['GET'])
def oauth2_authorize():
    url= oauth_util.get_oauth2_authorize_url(
         clientId= current_app.config['CLIENT_ID'], 
         remoteAuthorizeUrl=current_app.config['OAUTH2_ACCESS_URL'], 
         callbackUrl = current_app.config['OAUTH2_CALLBACK_URL'],
         )
    return render_template('jive/oauth_authorize.html', 
        app_name = current_app.config['APP_NAME'],
        oauth2_authorize_url = url
    );
    
@mod_jive.route('/oauth2/callback', methods=['POST'])
def oauth2_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not oauth_util.is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    
    print("Obtained Access Code [%s]" % code)
    
    accessToken = oauth_util.get_token(
      clientId = current_app.config['CLIENT_ID'],
      clientSecret = current_app.config['CLIENT_SECRET'],
      code = code,
      remoteAccessTokenUrl = current_app.config['OAUTH2_ACCESS_URL'],
      callbackUrl = current_app.config['OAUTH2_CALLBACK_URL'],                                 
    );
    
    # TODO: IMPLEMENT YOUR OWN PERSISTENCE STRATEGY
    current_app.config['OAUTH2_ACCESS_TOKEN'] = accessToken
    
    print("Obtained Access Token [%s]" % accessToken)

@mod_jive.route('/oauth2/access_token', methods=['GET'])
def oauth2_access_token():
    print("/oauth2/access_token called")
    
    
@mod_jive.route('/debug', methods=['GET'])
def debug():
    return render_template('jive/debug.html', 
        app_name = current_app.config['APP_NAME'],
        addon_details = current_app.config['ADD_ON_REGISTRATION'],
        tile_details = current_app.config['TILE_REGISTRATION']
    );