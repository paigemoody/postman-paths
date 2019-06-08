from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import json

from random import choice

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

        # return redirect(f"/user/{user.user_id}") 
        return redirect(f"/collections") 

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

    old_user_email = User.query.filter(User.email == email).first()

    old_user_username = User.query.filter(User.username == username).first()

    # try to get user associated with email from database
    if not old_user_email:

        if not old_user_username:
            # if no user returned: make a new user object with email, username and pw

            new_user = User(email=email,username=username,password=password)

            # new_user = User(email="hi@gmail",username="name",password="1234")

            # add database changes to staging  
            db.session.add(new_user)
            # commit db changes 
            db.session.commit()

            flash(f'Welcome {new_user.username}!')

    return redirect('/')


# @app.route("/user/<user_id>")
# @login_required
# def user_info(user_id):
#     """Show user info."""
    
#     # sqlalchemy database calls for user and user ratings
#     user = User.query.filter(User.user_id == user_id).one()
#     # ratings = db.session.query(Rating).filter(Rating.user_id == user_id).all()

#     return render_template('user.html',
#                             user=user)

@app.route("/collections")
@login_required
def collections_info():
    """Show user info."""
    
    # sqlalchemy database calls for user and user ratings
    # user = User.query.filter(User.user_id == user_id).one()

    return render_template('user.html')

@app.route('/mapview')
def mapview():
    """Map view."""

    return render_template("mapview.html")


@app.route('/route_geometry.geojson') # becaomes queue job, some job_id
def receive_bbox_geometry():
    """Get bbox from DOM, render route geometry from path scripts, 
    output geojson of route."""
    bbox_geometry = request.args.get('bbox_geometry')
    bbox = get_bbox_from_geojson(bbox_geometry)
    updated_graph_inst = get_eulerian_graph_edges(bbox, "osm")

    start_node = choice(list(updated_graph_inst.nodes_dict.keys()))
    
    euler_circuit_output_graph = make_euler_circuit(start_node, updated_graph_inst)

    nodes_geometry = euler_circuit_output_graph.node_geojson
    edges_geometry = euler_circuit_output_graph.edge_geojson
    route_geometry = euler_circuit_output_graph.route_geojson

    return jsonify({ 
        "bbox_geometry" : bbox_geometry
        ,"edges_geometry" : edges_geometry
        ,"nodes_geometry" : nodes_geometry
        , "route_geometry" : route_geometry 
        })



@app.route("/save_route.json", methods=["POST"])
@login_required
def save_route():
    """Save route data to db."""

    user_id = request.form['user_id']

    nodes_data = json.loads(request.form['nodes_data'])
    bbox_data = json.loads(request.form['bbox_data'])
    edges_data = json.loads(request.form['edges_data'])

    route_line_data = json.loads(request.form['route_line_data'])
    route_length = route_line_data['features'][0]['properties']['route_length_km']

    new_route_name = json.loads(request.form['new_route_name'])
    desination_collection_name = json.loads(request.form['destination_collection_name'])

    print(f"\n\n\n\n\nadding {new_route_name} to {desination_collection_name}")


    # get user object 
    user = User.query.filter(User.user_id == user_id).one()

    # get route id - to use at the end to add all the geometries
    route_id = None; 

    # check if user has collection with collection name 

        # use AND thing like: q.filter( (Employee.state == 'CA') & (Employee.salary > 70000) )

        # no --> make a collection by the new name 
            
            # add route to new collection
            # update route_id var 

        # yes --> 

            # check if route with name already exits 

                # no --> add route 

                # yes --> alert user that route had not been added 
                    # return false to alert user
                    # return jsonify({ 
                    #         "route_name" : new_route_name,
                    #         "success" : "false"
                    #         })

    # add geometries based on route id

    ## old stuff to re-og 
    # check if a route with that name already exits    
    route_check = Route.query.filter(Route.route_name == new_route_name).first()

    print("route_check",route_check)

    # if route name isn't already taken, create a new route in the collection
    if not route_check:

        random_tasked_to_name = choice(["Sam", "Jim", "Rachelle", "Noami", "Kate"])

        new_route = Route(route_name=new_route_name,
                            collection_id=collection_check.collection_id,
                            tasked_to=random_tasked_to_name) 

        # add to the session and commit so the route id can be used for 
        # the other data pieces 
        db.session.add(new_route)
        db.session.commit()

        # get route id from route that was just added? 

        route = Route.query.filter(Route.route_name == new_route_name).first()

        route_id = route.route_id

        # add bbox 
        new_box_geom = BboxGeometry(route_id=route_id,
                  bbox_geometry= bbox_data
                  )
        # add to the session and commit 
        db.session.add(new_box_geom)
        db.session.commit()

        # get route id for the route that was just added 
        new_route_geom = RouteGeometry(route_id=route_id,
                                       route_geometry=route_line_data)
        
        # add to the session and commit 
        db.session.add(new_route_geom)
        db.session.commit()

        new_nodes_geom = NodesGeometry( route_id=route_id,
                               nodes_geometry=nodes_data)

        db.session.add(new_nodes_geom)
        db.session.commit()

        new_edges_geom = EdgesGeometry(route_id=route_id,
                               edges_geometry=edges_data)

        db.session.add(new_edges_geom)
        db.session.commit()

    print("\n\n\ndone?")


    return jsonify({ 
        "route_name" : new_route_name,
        "success" : "true"
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


