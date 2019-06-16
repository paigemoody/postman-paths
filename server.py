from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify, send_file
from flask_debugtoolbar import DebugToolbarExtension

import json

from random import choice

from circuit_constructor import get_bbox_from_geojson, get_eulerian_graph_edges, make_euler_circuit

from pprint import PrettyPrinter as pprint

from random import choice 

from model import User, Collection, Route, BboxGeometry,EdgesGeometry,NodesGeometry, RouteGeometry, connect_to_db, db

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from werkzeug.security import generate_password_hash, check_password_hash


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
    return redirect('/login')

# DELETE LATER
@app.route('/test_map')
def test_map():
    """Test map."""
    return render_template('test_map.html')
# DELETE ^^^

@app.route('/login')
def get_login():
    """Display login page."""

    # if logged in, send to routes
    if current_user.is_authenticated: 
        print("\n\n\n\nLOGGED IN")
        print(current_user.username)
        return redirect('/collections')

    # if not logged in show login
    else: 
        print("\n\n\n\nNOT LOGGED IN")
        print(current_user)
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

    if user:

        if check_password_hash(user.password, password):

        # if user.password == password:

            user.is_authenticated = True 

            login_user(user)

            flash(f'Welcome {user.username}!') 

            # return redirect(f"/user/{user.user_id}") 
            return redirect(f"/collections") 

    flash('Wrong username and/or password')
    return redirect('/login')

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect('/login')

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

    # if username is taken, tell user and send them back to the login page
    if old_user_username:

        flash(f'Bummer .... {username} already taken!')

    else:
        
        if not old_user_email:
        # if email isn't already taken by an existing account

            # make a new user object with email, username and pw

            new_user = User(email=email,username=username,password=password)

            # new_user = User(email="hi@gmail",username="name",password="1234")

            # add database changes to staging  
            db.session.add(new_user)
            # commit db changes 
            db.session.commit()

            flash(f'Welcome {new_user.username}!')

            return redirect('/mapview')

    
    return redirect('/login')


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


@app.route('/generate_route_data.json') # make into queue job, some job_id
def calculate_route_data():
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

@app.route('/collections/get_route_data/<route_id>/route_geometry.json') # make into queue job, some job_id
@login_required
def get_existing_route_data(route_id):
    """Given route id, return route json"""

    route_geometry_obj = RouteGeometry.query.filter((RouteGeometry.route_id == route_id)).first()
    route_geojson = route_geometry_obj.route_geometry

    return jsonify(route_geojson)

@app.route('/collections/get_route_data/<route_id>/edges_geometry.json') # make into queue job, some job_id
@login_required
def get_existing_edges_data(route_id):
    """Given route id, return edges geometry json"""

    edges_geometry_obj = EdgesGeometry.query.filter((EdgesGeometry.route_id == route_id)).first()
    edges_geojson = edges_geometry_obj.edges_geometry

    return jsonify(edges_geojson)

@app.route('/collections/get_route_data/<route_id>/nodes_geometry.json') # make into queue job, some job_id
@login_required
def get_existing_nodes_data(route_id):
    """Given route id, return edges geometry json"""

    nodes_geometry_obj = NodesGeometry.query.filter((NodesGeometry.route_id == route_id)).first()
    nodes_geojson = nodes_geometry_obj.nodes_geometry

    return jsonify(nodes_geojson)

@app.route('/collections/get_route_data/<route_id>/animate_point_geometry.json') # make into queue job, some job_id
@login_required
def get_animate_point_data(route_id):
    """Given route id, return start point geometry json"""

    route_geometry_obj = RouteGeometry.query.filter((RouteGeometry.route_id == route_id)).first()
    
    route_geojson = route_geometry_obj.route_geometry

    first_point_geojson = {
            "type": "FeatureCollection",
            "features": [{
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": route_geojson['features'][0]['geometry']['coordinates'][0]
                }
            }]
        }

    print("\n\n\n\nfirst_point_geojson:",first_point_geojson)

    return jsonify(first_point_geojson)

@app.route('/collections/get_collection_data/<collection_id>/all_bbox_coordinates.json')
@login_required
def get_bounds_array_for_collection(collection_id):
    """Given route id, return edges geometry json"""

    # goal output -> return let fitBoundsArray = [[minX, minY] , [maxX, maxY]]

    fitBoundsArray = []

    # get all routes for collection:

    all_routes_in_collection = Route.query.filter(Route.collection_id == collection_id).all()

    all_lng = [] #x
    all_lat = [] #y
    
    for route in all_routes_in_collection:

        bbox_geometry = route.bbox.bbox_geometry

        coordinates_list = bbox_geometry['features'][0]['geometry']['coordinates'][0]

        for coordinate in coordinates_list:
            all_lng.append(coordinate[0])
            all_lat.append(coordinate[1])
        # all_route_ids_in_collection.append()

    min_x = min(all_lng)
    min_y = min(all_lat)
    max_x = max(all_lng)
    max_y = max(all_lat)


    fitBoundsArray = [[min_x, min_y] , [max_x, max_y]];

    return jsonify({"fitBoundsArray" : fitBoundsArray})

@app.route('/collections/get_route_data/<route_id>/route_bounds_geometry.json')
@login_required
def get_bounds_array_for_route(route_id):
    """Given route id, return bounds array json"""

    print(route_id)

    fitBoundsArray = []

    # get all routes for collection:

    route = Route.query.filter(Route.route_id == route_id).first()

    all_lng = [] #x
    all_lat = [] #y
    
    bbox_geometry = route.bbox.bbox_geometry

    coordinates_list = bbox_geometry['features'][0]['geometry']['coordinates'][0]

    for coordinate in coordinates_list:
        all_lng.append(coordinate[0])
        all_lat.append(coordinate[1])
        # all_route_ids_in_collection.append()

    min_x = min(all_lng)
    min_y = min(all_lat)
    max_x = max(all_lng)
    max_y = max(all_lat)


    fitBoundsArray = [[min_x, min_y] , [max_x, max_y]];

    return jsonify({"fitBoundsArray" : fitBoundsArray})

@app.route('/collections/get_collection_data/<collection_id>/all_routes.json') # make into queue job, some job_id
@login_required
def get_collection_routes_list(collection_id):
    """Given route id, return all routes in collection"""

    all_routes_in_collection = Route.query.filter(Route.collection_id == collection_id).all()

    all_route_ids_in_collection = []

    for route in all_routes_in_collection:

        all_route_ids_in_collection.append(route.route_id)

    print("\n\n\n\n", all_route_ids_in_collection)

    return jsonify({"route_ids" : all_route_ids_in_collection})

@app.route("/save_route.json", methods=["POST"])
@login_required
def save_route():
    """Save route data to db."""

    user_id = request.form['user_id']

    nodes_data = json.loads(request.form['nodes_data'])
    bbox_data = json.loads(request.form['bbox_data'])
    edges_data = json.loads(request.form['edges_data'])

    route_line_data = json.loads(request.form['route_line_data'])

    # route_length = route_line_data['features'][0]['properties']['route_length_km']

    route_length = json.loads(request.form['route_length'])

    new_route_name = json.loads(request.form['new_route_name'])
    desination_collection_name = json.loads(request.form['destination_collection_name'])

    print("\n\n\ndesination collection name:", desination_collection_name)

    print(f"\n\n\n\n\nadding {new_route_name} to {desination_collection_name}")


    # get user object 
    user = User.query.filter(User.user_id == user_id).one()

    # hard-code hack -- randomly select some name to assign the route to
    random_tasked_to_name = choice(["Sam", "Jim", "Rachelle", "Noami", "Kate"])

    # initialize route id - to use at the end to add all the geometries
    route_id = None; 

    # check if user has collection with collection name 
        # if it's a new coll collection_check will be None
    collection = Collection.query.filter((Collection.collection_name == desination_collection_name) & (Collection.user_id == user_id)).first()

    # if the collection is new
    if collection == None:

        # make collection
        new_collection = Collection(
                    user_id = user_id,
                    collection_name = desination_collection_name,
                    description = "" # need to add 
                    )

        db.session.add(new_collection)
        db.session.commit()

        # get collection just added to get the collection id from it 

        added_collection = Collection.query.filter(Collection.collection_name == desination_collection_name).first()

        # make route and add to collection 
        new_route = Route(route_name=new_route_name,
                            collection_id=added_collection.collection_id,
                            tasked_to=random_tasked_to_name) 

        # add to the session and commit so the route id can be used for 
        # the other data pieces 
        db.session.add(new_route)
        db.session.commit()

        # update route_id to be the id of the route just added 
        added_route = Route.query.filter(Route.route_name == new_route_name).first()
        route_id = added_route.route_id

    else:

        # check if a route of the new route name already exists in the db
        route = Route.query.filter((Route.route_name == new_route_name) & (Route.collection_id == collection.collection_id)).first()
        
        # if route already exists return success as false 

        if route != None:
            return jsonify({ 
                                "route_name" : new_route_name,
                                "success" : "false"
                                })

        # else add route to collection
        else:
            new_route = Route(route_name = new_route_name,
                            collection_id = collection.collection_id,
                            tasked_to = random_tasked_to_name) 

            # add to the session and commit so the route id can be used for 
            # the other data pieces 
            db.session.add(new_route)
            db.session.commit()

            # update route_id to be that of the added route
            # added_route = Route.query.filter((Route.route_name == new_route_name) & (Route.collection.user_id == user_id))
            added_route = Route.query.filter(Route.route_name == new_route_name).first()
            route_id = added_route.route_id
                    
    # add geometries based on route id

    # add bbox 
    new_box_geom = BboxGeometry(route_id=route_id,
              bbox_geometry= bbox_data
              )
    # add to the session and commit 
    db.session.add(new_box_geom)
    db.session.commit()

    # get route id for the route that was just added 
    new_route_geom = RouteGeometry(route_id=route_id,
                                   route_geometry=route_line_data,
                                   route_length=route_length)
    
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


