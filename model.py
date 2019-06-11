from flask import Flask

from flask_sqlalchemy import SQLAlchemy

import datetime 

# from geoalchemy2 import Geometry

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """User of app."""

    def __repr__(self): 
        """provide helpful represeation."""

        return f"<User user_id={self.user_id} email={self.email}>"

    __tablename__ = "users"

    user_id  = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), nullable=False)    
    email    = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(64), nullable=False)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self): # line 37
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

class Collection(db.Model):
    """Collection of routes."""

    def __repr__(self): 
        """provide helpful represeation."""

        return f"<Collection collection_id={self.collection_id} user_id={self.user_id}>"

    __tablename__ = "collections"

    collection_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    user_id       = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    collection_name = db.Column(db.String(100))
    description = db.Column(db.String(200), nullable=False)
    created_date = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)
    
    # define relationship with user table 
    user = db.relationship("User",
                           backref=db.backref("collections", 
                                              order_by=collection_id))

class Route(db.Model):
    """Individual Route."""

    def __repr__(self):
        """provide helpful represeation."""

        return f"<Route route_id={self.route_id} collection_id={self.collection_id}>"

    __tablename__ = "routes"

    route_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    route_name = db.Column(db.String(100))
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.collection_id'))
    created_date = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)
    route_complete = db.Column(db.Boolean, nullable=False, default=False)
    tasked_to = db.Column(db.String(100), nullable=True)

    # add route_complete boolean 
    # add tasked to - for tasking a route in a collection

    # define relationship with collections table
    collection = db.relationship("Collection",
                                        backref=db.backref("routes"),
                                                            order_by=route_id)

    # define relationship with bboxes table
    bbox = db.relationship("BboxGeometry", 
                            backref=db.backref("routes"), uselist = False)

    # define relationship with edges geometries table
    edges_geom = db.relationship("EdgesGeometry", 
                            backref=db.backref("routes"), uselist = False)

    # define relationship with nodes geometries table
    nodes_geom = db.relationship("NodesGeometry", 
                            backref=db.backref("routes"),uselist = False)

    # define relationship with route geometries table
    route_geom = db.relationship("RouteGeometry", 
                            backref=db.backref("routes"), uselist = False)


class BboxGeometry(db.Model):
    """Geometry of a bbox"""

    def __repr__(self):
        """provide helpful represeation."""

        return f"<Bbox bbox_id={self.bbox_id} route_id={self.route_id}>"

    __tablename__ = "bboxes"

    bbox_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
    bbox_geometry = db.Column(db.JSON, nullable = False)

class EdgesGeometry(db.Model):
    """Geometry of an edges feature collection"""

    def __repr__(self):
        """provide helpful represeation."""

        return f"<Edges Geometry edges_geom_idd={self.bbox_id} route_id={self.route_id}>"

    __tablename__ = "edges_geoms"

    edges_geom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
    edges_geometry = db.Column(db.JSON, nullable=False)

class NodesGeometry(db.Model):
    """Geometry of a nodes feature collection"""

    def __repr__(self):
        """provide helpful represeation."""

        return f"<Nodes Geometry nodes_geom_idd={self.bbox_id} route_id={self.route_id}>"

    __tablename__ = "nodes_geoms"

    nodes_geom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
    nodes_geometry = db.Column(db.JSON, nullable=False)


class RouteGeometry(db.Model):
    """Geometry of a route - for animation"""

    def __repr__(self):
        """provide helpful represeation."""

        return f"<Route Geometry route_geom_idd={self.route_geom_id} route_length={self.route_length} route_id={self.route_id}>"

    __tablename__ = "route_geoms"


    route_geom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
    route_geometry = db.Column(db.JSON, nullable=False)
    route_length = db.Column(db.Float, nullable=True)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///postman_paths'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")








