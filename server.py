from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import json

from circuit_constructor import get_bbox_from_geojson, get_eulerian_graph_edges, make_euler_circuit

from pprint import PrettyPrinter as pprint

from random import choice 

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


@app.route('/route_geometry.geojson')
def receive_bbox_geometry():
    """Get bbox from DOM, render route geometry from path scripts, 
    output geojson of route."""


    bbox_geometry = request.args.get('bbox_geometry')

    # print("\n\n\ntype(bbox_geometry):",type(bbox_geometry))

    # print("\n\nbbox geometry:",bbox_geometry)

    bbox = get_bbox_from_geojson(bbox_geometry)

    # print("bbox:", bbox)


    updated_graph_inst = get_eulerian_graph_edges(bbox, "osm")

    # print("\n\n\nupdated_graph_inst.edges_dict:",updated_graph_inst.edges_dict)

    start_node = choice(list(updated_graph_inst.nodes_dict.keys()))
    
    euler_circuit_output_graph = make_euler_circuit(start_node, updated_graph_inst)

    nodes_geometry = euler_circuit_output_graph.node_geojson

    route_geometry = euler_circuit_output_graph.edge_geojson

    # print("\n\n\n\nNODES GEOM:")
    # print(nodes_geometry)

    # print("\n\n\n\nROUTE GEOM:")
    # print(route_geometry)


    return jsonify({ 
        "bbox_geometry" : bbox_geometry
        ,"route_geometry" : route_geometry
        ,"nodes_geometry" : nodes_geometry
        })

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


