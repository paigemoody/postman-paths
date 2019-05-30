mapboxgl.accessToken = 'pk.eyJ1IjoicGFpZ2VlbW9vZHkiLCJhIjoiY2owbDcyejhvMDJwNzJ5cDR0YXE1aG10MCJ9.a-JLnrmMPSJNwOGQdloTDA';


// LOAD MAP 
var map = new mapboxgl.Map({
    container: 'map', // container id
    style: 'mapbox://styles/mapbox/satellite-v9', //hosted style id
    center: [-122.400932, 37.758250], // starting position is balloonicorn example route centr
    zoom: 15 // starting zoom
});


// DRAW BBOX 

var draw = new MapboxDraw({

    displayControlsDefault: false,

    controls: {
        polygon: true,
        trash: true
    }

}); 

map.addControl(draw);
 
// map.on('draw.create', updateStatus);
// map.on('draw.delete', updateStatus);
// map.on('draw.update', updateStatus);





// when bboxx is double-clicked, you have the 
// bbox data


map.on('draw.create', function(evt) {

    let data = draw.getAll();
    //const bboxGeometryJSON = JSON.stringify(data);??


    if (data.features.length > 0) {
    // if there is a bbox feature, show the calculate button 
        $('#calcuate-route-btn').removeAttr('style');

        // remove draw tool and add a new one with just a trashcan?
        // to limit drawing of more than one bbox

        // const formInputs = {
        //     bbox: bboxGeometryJSON
        // };

        //$.get('/bbox_geometry.geojson', {hi :"hi"}, sendAlert);
    } 

    else {

        if (e.type !== 'draw.delete') alert("Use the draw tools to draw a bbox!");
    }

})

// function to play route
function animateRoute(evt){
    let route = evt.data.routrgeometry

    // A single point that animates along the route.
    // Coordinates are initially set to the first coordinate 
    // in the route
    let point  = {
        "type": "FeatureCollection",
        "features": [{
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Point",
            "coordinates": route.features[0].geometry.coordinates[0]
            }
        }]
    }

    // get the full traversal distnace as line distance 
    // to use to create small line sections to animate - using steps
    let lineDistance = route.features[0]["properties"]["route_length_km"]

    // initialize an path list, segments along the route will be added to the path
    // each item in path will be one coordinatate
    var path = [];

    // Number of steps to use in the path and animation, more steps means
    // a smoother path and animation, but too many steps will result in a
    // low frame rate
    var steps = 500; // lower steps = faster movement along route 

    // make small route line segments to animate
    // add the coordinates of each segment to the path list 
    for (var i = 0; i < lineDistance; i += lineDistance / steps) {

        // i is the distance you've traveled along the route
        let input_line = route.features[0];

        const distance_along_line = i; 

        // turf.along takes a LineString and 
        // returns a Point at a specified distance along the line.
        var segment = turf.along(input_line, distance_along_line, 'kilometers');
        path.push(segment.geometry.coordinates);

        //  bug with not totally returning the original point
        // need to add something that forces the return
    }

    // Update the route with calculated path coordinates
    // route.features[0].geometry.coordinates = path;
    route.features[0].geometry.coordinates = path;

    // Used to increment the value of the point measurement against the route.
    let counter = 0 

    // map.on('load', 

    // function () {

    // console.log("\n\nadding source:", point)
    //     map.addSource('point', {
    //         "type": "geojson",
    //         "data": point
    //     });

    // console.log("adding layer")
    //     // add point to be animated to graph 
    //     map.addLayer({
    //         "id": "point",
    //         "source": "point",
    //         "type": "symbol",
    //         "layout": {
    //             "icon-image": "restaurant-seafood-15", // change later
    //             "icon-rotate": ["get", "bearing"],
    //             "icon-rotation-alignment": "map",
    //             "icon-allow-overlap": true,
    //             "icon-ignore-placement": true,
    //             "icon-size": 2
    //         }
    //     });


        function animate() {
            // Update point geometry to a new position based on counter denoting
            // the index to access the path.
            console.log("counter",counter)

            console.log("coords",route.features[0].geometry.coordinates[counter])

            console.log("coords count:",(route.features[0].geometry.coordinates).length)

            // what makes the icon move
            // need to control for the end of the route where you don't want
            // to index outside of the coordinates array
            if (counter < (route.features[0].geometry.coordinates).length) {
                point.features[0].geometry.coordinates = route.features[0].geometry.coordinates[counter];
            } else {
                point.features[0].geometry.coordinates = route.features[0].geometry.coordinates[counter-1];
            }; 
            
            point.features[0].properties.bearing = 0;
            // Update the source with this new data.
            map.getSource('point').setData(point);

            // Request the next frame of animation so long the end has not been reached.
            if (counter < steps) {
                requestAnimationFrame(animate);
            }

            counter = counter + 1;

            console.log("bearing:", point.features[0].properties.bearing);
        }

        animate(counter);

    // }

// );

}

//GET ROUTE CALCULATION

function addBboxAndRoute(displayGeojsons) {

    // remove draw function 
    // map.removeControl(draw);

    // hide calculate route button, show animate button
    $('#calcuate-route-btn').attr('style','display:none ;');
    $('#animate-route-btn').removeAttr('style');


    
    // get geometry feature collections back from get request and 
    // jsonify each

    // let bboxGeometry = JSON.parse(displayGeojsons['bbox_geometry']);
    let edgesGeometry = JSON.parse(displayGeojsons['edges_geometry']);
    let nodesGeometry = JSON.parse(displayGeojsons['nodes_geometry']);
    let routeGeometry = JSON.parse(displayGeojsons['route_geometry']);

    //  run animate route function - send route geometry to function
    // $('#animate-route-btn').on('click', handleBboxSend(routeGeometry));

    $('#animate-route-btn').click({routrgeometry : routeGeometry}, animateRoute);

    // reduce bbox opacity
    map.setPaintProperty('bbox-geometry', 'fill-opacity', .1);

    // console.log("\n\ntype bbox geom:", typeof bboxGeometry);
    // console.log("\n\ntype edges geom:", typeof edgesGeometry);
    

    console.log("\n\n\n nodes geometry", nodesGeometry);
    console.log("\n\n\n edges geometry", edgesGeometry);
    console.log("\n\n\n route geometry", routeGeometry);


    // console.log("\n\n\n start node", nodesGeometry['features'][0]['properties']['start_node'])

    // console.log("\n\n\n start node type", (typeof nodesGeometry['features'][0]['properties']['start_node']))
    
    //  add point to be animated to graph 
    let point  = {
        "type": "FeatureCollection",
        "features": [{
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Point",
            "coordinates": routeGeometry.features[0].geometry.coordinates[0]
            }
        }]
    }
    map.addSource('point', {
        "type": "geojson",
        "data": point
    });
    // add point to be animated to graph 
    map.addLayer({
        "id": "point",
        "source": "point",
        "type": "symbol",
        "layout": {
            "icon-image": "police-15", // change later
            // "icon-rotate": ["get", "bearing"],
            // "icon-rotation-alignment": "map",
            "icon-allow-overlap": true,
            "icon-ignore-placement": true,
            "icon-size": 2
        }
    });


    // add nodes feature collection to map

    map.addSource('nodes', {
        "type": "geojson",
        "data" : nodesGeometry
    });
    
    // add nodes layer as symbol type 
    map.addLayer({
        "id" : "nodes-geometry",
        "type" : "symbol",
        "source" : "nodes",
        "layout": {
            "icon-image": [
                'match',
                ['get', 'start_node'],
                'true', "star-15",
                'false', "circle-11",
                "circle-11"
            ],

            "icon-size" : [
                'match',
                ['get', 'was_odd'],
                'true', 1,
                'false', .4,
                .6
            ],
            "text-field": "{visit_order}",
            "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
            "text-offset": [0, 0.6],
            "text-anchor": "top"
            },
        paint: {
            "text-color": "#000000",
            "text-halo-color": "#ffffff",
            "text-halo-width": 1
          }
    }, "point");


    // add route feature collection to map

    map.addSource('route', { //  bbox in this case is a variable that is a feature collection
        "type": "geojson",
        "data": edgesGeometry
        });

    map.addLayer({
        "id": "route-geometry", // rename?
        "type": "line",
        "source": "route", 
        "paint": {
            // set line color based on number of traversals, to highlight which streets to 
            // traverse twice
            "line-color" : [
                'match',
                ['get', 'num_traversals'],
                1, 'rgba(0,0,205,0.3)', 
                // 1, '#e55e5e', // pink
                // 2, '#fbb03b', // orange
                2, 'rgba(0,0,205,0.6)',
                // 3, '#00FF00', // green
                3, 'rgba(0,0,205,0.9)',
                'rgba(0,0,205,1)',
                // '#123c69' // blue
            ],
            "line-width": 8,
            "line-opacity": 1
        }
    }, "nodes-geometry"); // second agument determines which layer should be direcly above the bbox layer


}

// when the calculate route button is clicked, send bbox geometry to 

function handleBboxSend(evt) {

    let bbox = draw.getAll();

    // add bbox to map 
    map.addSource('bbox', { //  bbox in this case is a variable that is a feature collection
        "type": "geojson",
        "data": bbox
        });

    map.addLayer({
        "id": "bbox-geometry", // rename?
        "type": "fill", // bbox is a polygon
        "source": "bbox", 
        "paint": {
            'fill-color': '#FFE400',
            'fill-opacity': 0.3,
        }
    }); 

    // remove ability to draw polygon after the bbox polygon is added 
    map.removeControl(draw);

    bbox = JSON.stringify(bbox);

    const formInputs = {
        'bbox_geometry' : bbox
      };

    // the outout of the get request (what is returned from the url route)
    // is sent as the parameter to addBboxAndRoute
    $.get('/route_geometry.geojson', formInputs, addBboxAndRoute);

    
}

$('#calcuate-route-btn').on('click', handleBboxSend);

// $('#change-style-b').on('click', function() {
   
//         map.setStyle('mapbox://styles/paigeemoody/cjve0tvkzhbdf1fpacmnwbc88')
//     });

// $('#change-style-s').on('click', function() {
   
//         map.setStyle('mapbox://styles/mapbox/satellite-v9')
//     });

// map.addControl(new mapboxgl.GeolocateControl({
//     positionOptions: {
//         enableHighAccuracy: true
//     },
//     trackUserLocation: true
// }));
