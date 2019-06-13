mapboxgl.accessToken = 'pk.eyJ1IjoicGFpZ2VlbW9vZHkiLCJhIjoiY2owbDcyejhvMDJwNzJ5cDR0YXE1aG10MCJ9.a-JLnrmMPSJNwOGQdloTDA';
var map = new mapboxgl.Map({
    container: 'map', // container id
    style: 'mapbox://styles/paigeemoody/cjwjzqywq2orj1dqqvdvwchhm',
    center: [-122.453554,37.762436], // starting position [lng, lat]
    zoom: 10 // starting zoom
});

const collectionButtons = document.querySelectorAll('.tablinks')

collectionButtons.forEach(collectionButton => {

    collectionButton.addEventListener('click', function (event) {  
        // prevent browser's default action
        event.preventDefault();

        collectionId = this.id

        console.log(collectionId)
        // get the id of the collection
        showAllRoutes(this, collectionId); // 'this' refers to the current button on for loop
   
    }, false);
})

// map.on("load", function() {
function showAllRoutes(evt, collectionId) {

    $.getJSON(`/collections/get_collection_data/${collectionId}/all_routes.json`, function(collectionJson) {
        // get obj of all layers currently on map 
        const currentSources = map.getStyle().sources;
        // get array of sources - to later determine if any need to be removed 
        const currentSourcesArray = Object.keys(currentSources);

        currentSourcesArray.forEach(source => {
            // remove all current sources & layers 
            if (source != "composite") {
                map.removeLayer(source);
                map.removeSource(source);
            }

        });

        const routeIds = collectionJson['route_ids'];

        // get all routeCoords from all node geometries in collection
        // to be used to zoom map
        let allBboxCoords = []
        
        routeIds.forEach(route_id => {

            const id = route_id;
            // // POINT FOR ANIMATION 
            animationId = `point${id}`
            animationSource = `/collections/get_route_data/${id}/animate_point_geometry.json`

            map.addSource(animationId, {
                "type": "geojson",
                "data": animationSource
            });
            // add point to be animated to graph 
            map.addLayer({
                "id": animationId,
                "source": animationId,
                "type": "symbol",
                "layout": {
                    'visibility': 'visible',
                    "icon-image": "police-15", // change later
                    // "icon-rotate": ["get", "bearing"],
                    // "icon-rotation-alignment": "map",
                    "icon-allow-overlap": true,
                    "icon-ignore-placement": true,
                    "icon-size": 2
                }
            });
            
            //NODES
            nodesId = `nodes${id}`
            nodesSource = `collections/get_route_data/${id}/nodes_geometry.json`

            map.addSource(nodesId, {
                "type": "geojson",
                "data" : nodesSource
            });

            map.addLayer({
                "id" : nodesId,
                // "type" : "symbol",
                "type" : "symbol",
                "source" : nodesId,
                "layout": {
                    'visibility': 'none', //hide nodes layer at first 
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
            }, animationId); // add point layer order ref 

            // EDGES
            edgesId = `edges${id}`
            edgesSource = `collections/get_route_data/${id}/edges_geometry.json`

            map.addSource(edgesId, {
                "type": "geojson",
                "data": edgesSource
            });

            map.addLayer({
                "id": edgesId,
                "type": "line",
                "source": edgesId, 
                "layout": {'visibility': 'visible'},
                "paint": {
                    // set line color based on number of traversals, to highlight which streets to 
                    // traverse twice
                    // "line-color" : [
                    //     'match',
                    //     ['get', 'num_traversals'],
                    //     1, 'rgba(0,0,205,0.3)', 
                    //     // 1, '#e55e5e', // pink
                    //     // 2, '#fbb03b', // orange
                    //     2, 'rgba(0,0,205,0.6)',
                    //     // 3, '#00FF00', // green
                    //     3, 'rgba(0,0,205,0.9)',
                    //     'rgba(0,0,205,1)',
                    //     // '#123c69' // blue
                    // ],
                    "line-color" : 'rgba(0,0,205,0.3)',
                    "line-width": 3,
                    "line-opacity": 1
                }
            }, nodesId);
  
            // ROUTE GEOM FOR ANIMATION
            routeId = `route${id}`
            routeSource = `collections/get_route_data/${id}/route_geometry.json`

            map.addSource(routeId, {
                "type": "geojson",
                "data": routeSource
            });

            map.addLayer({
                "id": routeId, // rename?
                "type": "line",
                "source": routeId, 
                "layout" : {'visibility': 'visible'},
                "paint": {
                    "line-color" : 'rgba(0,0,205,0)',
                    }
            });    

            

        });

        // BBOX to use for centering map 
            // add all bbox coordinates to allCoords array

        bboxSource = `/collections/get_collection_data/${collectionId}/all_bbox_coordinates.json`

        $.get(bboxSource, function (fitBoundsJson) {

            fitBoundsArray = fitBoundsJson["fitBoundsArray"];

            map.fitBounds(fitBoundsArray, {padding: {
                                    top: 80, 
                                    bottom:100, 
                                    left: 60, 
                                    right: 60}
                    });
        });
    
    });   
};

// handle route button click - show details of route 

const routeButtons = document.querySelectorAll('.animate');

routeButtons.forEach(routeButton => {

    routeButton.addEventListener('click', function (event) {  
        // prevent browser's default action
        event.preventDefault();

        let routeId = this.id

        bboxSource = `/collections/get_route_data/${routeId}/route_bounds_geometry.json`

        $.get(bboxSource, function (fitBoundsJson) {

            fitBoundsArray = fitBoundsJson["fitBoundsArray"];

            map.fitBounds(fitBoundsArray, {padding: {
                                    top: 40, 
                                    bottom:50, 
                                    left: 30, 
                                    right: 30}
                    });
        });

        $.getJSON(`/collections/get_route_data/${routeId}/route_geometry.json`, function(routeJson) {
            
            const route = routeJson;

            const startCoordinate = route.features[0].geometry.coordinates[0];

            console.log("route coords:", startCoordinate)

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
                    "coordinates": startCoordinate
                    }
                }]
            }

            let lineDistance = route.features[0]["properties"]["route_length_km"];

            console.log('lineDistance', lineDistance);
            // initialize an path list, segments along the route will be added to the path
            // each item in path will be one coordinatate
            let path = [];
            // Number of steps to use in the path and animation, more steps means
            // a smoother path and animation, but too many steps will result in a
            // low frame rate
            const steps = 500; // lower steps = faster movement along route 
            // make small route line segments to animate
            // add the coordinates of each segment to the path list 
            for (var i = 0; i < lineDistance; i += lineDistance / steps) {

                // i is the distance you've traveled along the route
                let input_line = route.features[0];

                const distance_along_line = i; 

                // turf.along takes a LineString and 
                // returns a Point at a specified distance along the line.
                let options = {units: 'kilometers'};

                let segment = turf.along(input_line, distance_along_line, options);

                console.log(segment)

                path.push(segment.geometry.coordinates);
                //  bug with not totally returning the original point
                // need to add something that forces the return
            }

            // Update the route with calculated path coordinates
            // route.features[0].geometry.coordinates = path;
            route.features[0].geometry.coordinates = path;

            // Used to increment the value of the point measurement against the route.
            let counter = 0

            function animate() {
                // Update point geometry to a new position based on counter denoting
                // the index to access the path.
                // what makes the icon move
                // need to control for the end of the route where you don't want
                // to index outside of the coordinates array
                if (counter < (route.features[0].geometry.coordinates).length) {
                    point.features[0].geometry.coordinates = route.features[0].geometry.coordinates[counter];
                } else {
                    point.features[0].geometry.coordinates = route.features[0].geometry.coordinates[counter-1];
                }; 
                
                point.features[0].properties.bearing = 0;

                // Update the animation point with the new data.

                let sourceId = `point${routeId}`

                map.getSource(sourceId).setData(point);

                // Request the next frame of animation so long the end has not been reached.
                if (counter < steps) {
                    requestAnimationFrame(animate);
                }

                counter = counter + 1;
            }
            animate(counter);
        });

        
    }, false);
})