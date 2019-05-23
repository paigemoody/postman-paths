from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import json

from pprint import pprint

# from classes import 

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


# possibly don't need this 
# @app.route('/bbox_geometry.geojson')
# def get_bbox_geometry():
#     """Get bbox geometry from DOM, render json at route."""

#     bbox_geometry = request.args.get('hi')

#     print(bbox_geometry)

#     return jsonify(bbox_geometry)

@app.route('/route_geometry.geojson')
def receive_bbox_geometry():
    """Get bbox from DOM, render route geometry from path scripts, 
    output geojson of route."""


    bbox_geometry = request.args.get('bbox_geometry')

    print("type:", type(bbox_geometry))
    # pprint(bbox_geometry)

    # TO DO: RUN reoute creation function!
    # route = my_funct(bbox_geometry)

    # scrap to test
    with open('static/example_complete_route.geojson') as json_file:  
        route_geometry = json.dumps(json.load(json_file))

    print("\n\ntype bbox:", type(bbox_geometry))
    print(bbox_geometry)

    print("\n\ntype route:", type(route_geometry))
    print(route_geometry)

    return jsonify({ "bbox_geometry" : bbox_geometry,
        "route_geometry" : route_geometry})

# @app.route('/route_geometry.geojson', methods = ['GET'])
# def get_route_geometry():
#     """Get bbox from DOM, render route geometry from path scripts, 
#     output geojson of route."""


#     # bbox_geometry = request.form.get('bbox_geometry')

#     # print("type:", type(bbox_geometry))
#     # print(bbox_geometry)

#     # #  run route creation function

#     # route = my_funct(bbox_geometry)

#     # return("SOMETHING")

#     with open('static/example_complete_route.geojson') as json_file:  
#         data = json.load(json_file)

#     return jsonify(data)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.debug = True
    # make sure templates, etc. are not cached in debug mode
    # app.jinja_env.auto_reload = app.debug

    # connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')