from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import json

from circuit_constructor import get_bbox_from_geojson, get_eulerian_graph_edges, make_euler_circuit

from pprint import PrettyPrinter as pprint

from random import choice 

from model import User, Collection, Route, BboxGeometry,EdgesGeometry,NodesGeometry, RouteGeometry, connect_to_db, db

from flask_login import LoginManager, login_user, logout_user, login_required


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


####################################
# Configuration for login handling
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    """Requirement for flask_login."""

    return User.query.filter(User.user_id == user_id).first()


####################################
@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/login')
def get_login():
    """Display login page."""

    return render_template("login.html")

@app.route('/login_submission', methods=['POST'])
def login_sub():
    """Process login."""

    username = request.form.get('username')
    password = request.form.get('password')

    print("\n\nusername",username)
    print("\n\npassword",password)


    user = User.query.filter(User.username == username).first()

    # user = User.query.filter(User.user_id == user_id).one() ??

    print("\n\n\nuser:",user)

    if user.password == password:

        user.is_authenticated = True 

        login_user(user)

        flash('Login success!') 

        return redirect(f"/user/{user.user_id}") 

    alert('Wrong username and/or password')
    return redirect('/login')

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect('/')

@app.route("/register", methods=["POST"])
def register_process():
    """Processes registration request."""

    username=request.form['username']
    email=request.form['email']
    password=request.form['password']

    print("\n\n\nemail", email)

    old_user = User.query.filter(User.email == email).first()

    print("old_user", old_user)

    # try to get user associated with email from database
    if not old_user:
        # if no user returned: make a new user object with email, username and pw

        new_user = User(email=email,username=username,password=password)

        # new_user = User(email="hi@gmail",username="name",password="1234")

        # add database changes to staging  
        db.session.add(new_user)
        # commit db changes 
        db.session.commit()

        flash(f'Welcome {new_user.username}!') 

    return redirect('/')


@app.route("/user/<user_id>") # add @login_required
def user_info(user_id):
    """Show user info."""
    
    # sqlalchemy database calls for user and user ratings
    user = User.query.filter(User.user_id == user_id).one()
    # ratings = db.session.query(Rating).filter(Rating.user_id == user_id).all()
    return render_template('user.html',
                            user=user)

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

    print("\n\nbbox geometry:",bbox_geometry)

    bbox = get_bbox_from_geojson(bbox_geometry)

    # print("bbox:", bbox)


    updated_graph_inst = get_eulerian_graph_edges(bbox, "osm")

    # print("\n\n\nupdated_graph_inst.edges_dict:",updated_graph_inst.edges_dict)

    start_node = choice(list(updated_graph_inst.nodes_dict.keys()))
    
    euler_circuit_output_graph = make_euler_circuit(start_node, updated_graph_inst)

    nodes_geometry = euler_circuit_output_graph.node_geojson

    edges_geometry = euler_circuit_output_graph.edge_geojson

    route_geometry = euler_circuit_output_graph.route_geojson

    print("\n\n\n\nbbox_geometry:")
    print(bbox_geometry)

    # print("\n\n\n\nnodes geom:")
    # print(nodes_geometry) 

    # print("\n\n\n\nedges_geometry")
    # print(edges_geometry)

    # print("\n\n\n\nroute_geometry")
    # print(route_geometry)


    return jsonify({ 
        "bbox_geometry" : bbox_geometry
        ,"edges_geometry" : edges_geometry
        ,"nodes_geometry" : nodes_geometry
        , "route_geometry" : route_geometry 
        })

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    
    app.debug = True
    # make sure templates, etc. are not cached in debug mode

    app.jinja_env.auto_reload = app.debug
    
    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5001, host='0.0.0.0')


