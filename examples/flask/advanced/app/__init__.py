# Import flask and template operators
from flask import Flask, request, redirect, url_for, send_from_directory

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_register.controllers import mod_register as register_module

# Register blueprint(s)
app.register_blueprint(register_module)
# app.register_blueprint(xyz_module)
# ..

#registering last
#see: http://codepen.io/asommer70/post/serving-a-static-directory-with-flask
@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)
