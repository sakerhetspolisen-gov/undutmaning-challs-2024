# routes/error_handlers.py
from flask import render_template_string, request
from urllib.parse import unquote
from flaskpost import app

@app.errorhandler(404)
def page_not_found(error):
    url = unquote(request.url)
    return render_template_string("<h1>URL %s not found</h1><br/>" % url), 404

