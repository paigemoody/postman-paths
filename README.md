
<p align="center">
	<img src="https://user-images.githubusercontent.com/25571355/59734595-eae75900-9206-11e9-8eca-4f89355e1058.png">
</p>
<h4 align="center">
	weave
</h4>
<p align="center">
helps community organizers improve canvassing outreach by generating optimized walking routes, guaranteed to take volunteers down every street, past every door, in an area.
</p>



![](homepage.gif)




**Route Generator** gets the shortest route to walk all roads in a drawn bbox.<br><br>

_Draw a polygon around the map area you'd like to cover. Weave then uses the [Chinese Postman graph traversal algorithm](https://en.wikipedia.org/wiki/Route_inspection_problem) to generate the shortest walking route that covers all roads within the given bounds. Then watch an animated walker traverse the calculated and save the route for later use by actual humans._

![](route_creation.gif)

**Collections** organize saved routes.

![](collections.gif)

*(check out a full demo [here](https://www.youtube.com/watch?v=u1m2kKUy4L0))*

## Tech Stack
Python, NetworkX, OSMnx, Shapely, PostgreSQL, SQLAlchemy, Flask, JavaScript (AJAX, JSON), JQuery, Turf.js, Mapbox GL JS, Jinja, HTML, CSS

## Getting Started

These instructions will get you a copy of the project up and running on your local machine with a sample database.

### Prerequisites

```
python3.7
postgresql
```

### Install dependencies 

`$ pip3 install -r requirements.txt`


### Run locally

**1.** (optional) Seed database with sample data.

	$ python3 seed.py

**2.** Create `sercrets.sh` file in root directory. 

**3.** Add `export flask_session_key="<some secret key>"` to `secrets.sh` *Note: this is required to run the Flask server.*

**4.** Connect `secrets.sh`. 

	$ source secrets.sh

	
**5.** Run server.

	$ python3 server.py

## Running the tests

Currently testing for the app is focused on unit tests for the backend graph constructor and circuit constructor scripts. Full test coverage is WIP. 


## Author

**[Paige Moody](https://www.linkedin.com/in/paige-moody)** 


## Acknowledgments

Shoutout to all the awesome people of [Hackbright](https://hackbrightacademy.com/) for their support and guidance on this project!
