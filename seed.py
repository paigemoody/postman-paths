"""Utility file to seed postman_routes database data in seed_data/"""

from sqlalchemy import func
from model import User, Collection, Route, BboxGeometry,EdgesGeometry,NodesGeometry,RouteGeometry
import datetime
from model import connect_to_db, db
from server import app
import json


def load_users():
    print("USERS") 

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/users"):
        row = row.rstrip()
        user_id, username, email, password = row.split("|")

        user = User(user_id=user_id,
                    username=username,
                    email=email,
                    password=password)

        # add to the session 
        db.session.add(user)

    # commit data
    db.session.commit()

def load_collections():
    print("COLLECTIONS")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate collections
    Collection.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/collections"):
        
        row = row.rstrip()

        collection_id, user_id, collection_name, description= row.split("|")

        collection = Collection(collection_id=collection_id,
                    user_id=user_id,
                    collection_name=collection_name,
                    description = description
                    )

        # add to the session 
        db.session.add(collection)

    # commit data
    db.session.commit()
     

def load_routes():
    print("ROUTES")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate routes
    Route.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/routes"):
        
        row = row.rstrip()

        route_id, route_name, collection_id, tasked_to = row.split("|")

        route = Route(route_id=route_id,
                                route_name=route_name,
                                collection_id=collection_id,
                                tasked_to=tasked_to)

        # add to the session 
        db.session.add(route)

    # commit data
    db.session.commit()

def load_bbox_geoms():
    print("BBOXES") 

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate bboxes
    BboxGeometry.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/bboxes"):
        
        row = row.rstrip()

        bbox_id, route_id, bbox_geometry = row.split("|")

        # loads to make sure postgres reads as json not string
        bbox_geometry = json.loads(bbox_geometry) 


        bbox = BboxGeometry(bbox_id=bbox_id,
                      route_id=route_id,
                      bbox_geometry=bbox_geometry
                      )

        # add to the session 
        db.session.add(bbox)

    # commit data
    db.session.commit()

def load_edges_geoms():
    print("EDGES_GEOMS") 

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate edges geometries
    EdgesGeometry.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/edges_geoms"):
        
        row = row.rstrip()

        edges_geom_id, route_id, edges_geometry = row.split("|")

        # print(edges_geom_id, route_id, edges_geometry )

        edges_geometry = json.loads(edges_geometry)

        edges_geom = EdgesGeometry(edges_geom_id=edges_geom_id,
                                   route_id=route_id,
                                   edges_geometry=edges_geometry)
        # add to the session 
        db.session.add(edges_geom)

    # commit data
    db.session.commit()

def load_nodes_geoms():
    print("NODES_GEOMS") 

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate nodes geometries 
    NodesGeometry.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/nodes_geoms"):
        
        row = row.rstrip()

        nodes_geom_id, route_id, nodes_geometry = row.split("|")

        nodes_geometry = json.loads(nodes_geometry)

        nodes_geom = NodesGeometry( nodes_geom_id=nodes_geom_id,
                                   route_id=route_id,
                                   nodes_geometry=nodes_geometry)
        # add to the session 
        db.session.add(nodes_geom)

    # commit data
    db.session.commit()

def load_routes_geoms():
    print("ROUTES_GEOMS")  

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate nodes geometries 
    RouteGeometry.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/route_geoms"):
        
        row = row.rstrip()

        route_geom_id, route_id, route_length ,route_geometry = row.split("|") # add length 

        print(route_length)

        route_geometry = json.loads(route_geometry)

        route_geom = RouteGeometry( route_geom_id=route_geom_id,
                                    route_id=route_id,
                                    route_geometry=route_geometry,
                                    route_length=route_length) # add length 
        # add to the session 
        db.session.add(route_geom)

    # commit data
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_collection_id():
    """Set value for the next collection_id after seeding database"""

    result = db.session.query(func.max(Collection.collection_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('collections_collection_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_route_id():
    """Set value for the next route_id after seeding database"""

    result = db.session.query(func.max(Route.route_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('routes_route_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_bbox_id():
    """Set value for the next bbox_id after seeding database"""

    result = db.session.query(func.max(BboxGeometry.bbox_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('bboxes_bbox_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_edges_id():
    """Set value for the next bbox_id after seeding database"""

    result = db.session.query(func.max(EdgesGeometry.edges_geom_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('edges_geoms_edges_geom_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_nodes_id():
    """Set value for the next bbox_id after seeding database"""

    result = db.session.query(func.max(NodesGeometry.nodes_geom_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('nodes_geoms_nodes_geom_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_routes_id():
    """Set value for the next bbox_id after seeding database"""

    result = db.session.query(func.max(RouteGeometry.route_geom_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('route_geoms_route_geom_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

     # In case tables haven't been created, create them
    db.create_all()

     # Import different types of data
    load_users()
    load_collections()

    load_routes()
    load_bbox_geoms()
    load_edges_geoms()
    load_nodes_geoms()
    load_routes_geoms()

    # set pk values to be able to auto increment after seeding 
    set_val_user_id()
    set_val_collection_id()
    set_val_route_id()
    set_val_bbox_id()
    set_val_edges_id()
    set_val_nodes_id()
    set_val_routes_id()

