"""Utility file to seed postman_routes database data in seed_data/"""

from sqlalchemy import func
from model import User, Collection, Route, BboxGeometry,EdgesGeometry,NodesGeometry,RouteGeometry
import datetime
from model import connect_to_db, db
from server import app


def load_users():
    print("USERS") 

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/users"):
        row = row.rstrip()
        user_id, email, password = row.split("|")

        user = User(user_id=user_id,
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

def load_bbox_geoms():
    print("BBOXES") 

def load_edges_geoms():
    print("EDGES_GEOMS") 

def load_nodes_geoms():
    print("NODES_GEOMS") 

def load_routes_geoms():
    print("ROUTES_GEOMS")  


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
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