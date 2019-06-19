# weave

Weave helps community organizers improve canvassing outreach by generating optimized walking routes, guaranteed to take volunteers down every street, past every door, in an area. 

First draw a polygon around the map area you'd like to cover. Weave then uses the [Chinese Postman graph traversal algorithm](https://en.wikipedia.org/wiki/Route_inspection_problem) to generate the shortest walking route that covers alls roads within the given bounds. You can then watch an animated walker traverse the calculated path for you and you can save the route for later use by actual humans.

<video src="static/style/readme.mp4" width="500" height="300" controls preload></video>

## Tech Stack
Python, NetworkX, OSMnx, Shapely, PostgreSQL, SQLAlchemy, Flask, JavaScript (AJAX, JSON), JQuery, Turf.jgs, Mapbox GL JS, Jinja, CSS

## Getting Started

These instructions will get you a copy of the project up and running on your local machine with a sample database.

### Prerequisites

```
python3.7
postgresql
```

### Install dependencies 

```
pip3 install -r requirements.txt
```

## Running the tests

Currently testing for the app is focused on unit tests for the backend graph constructor and circuit constructor scripts. Full test coverage is WIP. 


## Author

**[Paige Moody](https://www.linkedin.com/in/paige-moody)** 


## Acknowledgments

Shoutout to all the awesome people of [Hackbright](https://hackbrightacademy.com/) for their support and guidance on this project!
