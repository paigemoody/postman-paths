from flask_sqlalchemy import SQLAlchemy

from GeoAlchemy2 import Geometry

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
    email    = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(64), nullable=False)

class RouteCollection(db.Model):
    """Collection of routes."""

    def __repr__(self): 
        """provide helpful represeation."""

        return f"<RouteCollection collection_id={self.collection_id} user_id={self.user_id}>"

    __tablename__ = "route_collections"

    collection_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    collecion_name = db.Column(db.String(100))

    # define relationship with user table 
    user = db.relationship("User",
                           backref=db.backref("route_collections", 
                                              order_by=collection_id))

class Route(db.Model):
    """Individual Route."""

    def __repr__(self):
        """provide helpful represeation."""

        return f"<Route route_id={self.route_id} collection_id={self.collection_id}>"

    __tablename__ = "routes"

    route_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('route_collections.collection_id'))
    route_name = db.Column(db.String(100))

    # define relationship with route_collections table
    route_collection = db.relationship("RouteCollection",
                                        backref=db.backref("routes"),
                                                            order_by=route_id)


class BboxGeometry(db.Model):
    """Geometry of a bbox"""

    def __repr__(self):
        """provide helpful represeation."""

        return f"<Bbox bbox_id={self.bbox_id} route_id={self.route_id}>"

    __tablename__ = "bboxes"

    bbox_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    bbox_geometry = db.Column(db.JSON)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))

    bbox_wkb_geometry = db.Column(Geometry("GEOMETRYCOLLECTION"))

    # define relationship with route table
    route_collection = db.relationship("Route",
                                        backref=db.backref("bboxes"),
                                                            order_by=bbox_id)


class EdgesGeometry(db.Model):
    """Geometry of an edges feature collection"""

    def __repr__(self):
        """provide helpful represeation."""

        return f"<Edges Geometry edges_geom_idd={self.bbox_id} route_id={self.route_id}>"

    __tablename__ = "edges_geoms"

    edges_geom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
   
    edges_wkb_geometry = db.Column(Geometry("GEOMETRYCOLLECTION"))
    # edges_geometry = db.Column(db.JSON)

    # define relationship with route table
    route_collection = db.relationship("Route",
                                        backref=db.backref("edges_geoms"),
                                                            order_by=edges_geom_id)

class NodesGeometry(db.Model):
    """Geometry of a nodes feature collection"""

    def __repr__(self):
        """provide helpful represeation."""

        return f"<Nodes Geometry nodes_geom_idd={self.bbox_id} route_id={self.route_id}>"

    __tablename__ = "nodes_geoms"

    nodes_geom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
   
    nodes_wkb_geometry = db.Column(Geometry("GEOMETRYCOLLECTION"))
    # nodes_geometry = db.Column(db.JSON)

    # define relationship with route table
    route_collection = db.relationship("Route",
                                        backref=db.backref("nodes_geoms"),
                                                            order_by=nodes_geom_id)


class RouteGeometry(db.Model):
    """Geometry of a route - for animation"""

    def __repr__(self):
        """provide helpful represeation."""

        return f"<Route Geometry route_geom_idd={self.bbox_id} route_length={self.route_length} route_id={self.route_id}>"

    __tablename__ = "route_geoms"

    route_geom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))

    route_length = db.Column(db.Integer, nullable=False)
    route_wkb_geometry = db.Column(Geometry("GEOMETRYCOLLECTION"))

    # define relationship with route table
    route_collection = db.relationship("Route",
                                        backref=db.backref("route_geoms"),
                                                            order_by=route_geom_id)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///postman_paths'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")








