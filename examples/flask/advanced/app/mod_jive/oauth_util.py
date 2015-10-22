import urllib
import requests
import requests.auth

def get_oauth2_authorize_url(clientId, remoteAuthorizeUrl,callbackUrl, state=None):
    save_created_state(state)
    params = {
      "client_id": clientId,
      "response_type": "code",
      "state": state,
      "redirect_uri": callbackUrl,
      "duration": "temporary",
      "scope": "identity"
    }
    if not state:
        params['state'] = ""
        
    url = remoteAuthorizeUrl + "?" + urllib.urlencode(params)
    return url

def get_token(clientId,clientSecret,code,remoteAccessTokenUrl,callbackUrl):
    client_auth = requests.auth.HTTPBasicAuth(clientId, clientSecret)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": callbackUrl}
    response = requests.post(remoteAccessTokenUrl,
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]

def save_created_state(state):
    pass

def is_valid_state(state):
    return True