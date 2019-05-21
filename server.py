from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/mapview')
def mapview():
    """Map view."""

    return render_template("mapview.html")


@app.route('/route_geometry.geojson')
def route_geometry():
    """Route geometry."""

    with open('static/example_complete_route.geojson') as json_file:  
        data = json.load(json_file)

    return jsonify(data)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')