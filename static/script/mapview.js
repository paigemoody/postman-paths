
mapboxgl.accessToken = 'pk.eyJ1IjoicGFpZ2VlbW9vZHkiLCJhIjoiY2owbDcyejhvMDJwNzJ5cDR0YXE1aG10MCJ9.a-JLnrmMPSJNwOGQdloTDA';

//------------ LOAD MAP ------------\\
var map = new mapboxgl.Map({
    container: 'map', // container id
    style: 'mapbox://styles/paigeemoody/cjwygdg6mkbna1co7unnuchl6',
    center: [-122.41812145048675, 37.77818979943683],
    zoom: 14
});

// give instructions on load
map.on('load', function() {
    alert("Use the polygon tool to draw a bounding box!")

    // add image that will be used for animation symbol
    map.loadImage('/static/style/person_clipboard_teal.png', function(error, image) {
        map.addImage('person', image)
    });
})

//------------DRAWING TOOLS------------\\
var draw = new MapboxDraw({
    displayControlsDefault: false,
    controls: {
        polygon: true,
        trash: true
    }
}); 
map.addControl(draw);
// when bboxx is double-clicked, a create event happens
map.on('draw.create', function(evt) {
    let data = draw.getAll();

    if (data.features.length > 0) {
    // if there is a bbox feature, show the calculate button 
        $('#calcuate-route-btn').removeAttr('style');
        // remove draw tool and add a new one with just a trashcan?
        // to limit drawing of more than one bbox
    } else {
        if (e.type !== 'draw.delete') alert("Use the draw tools to draw a bbox!");
    }
})

//------------ BUTTONS TOGGLES------------\\
// Remove save route button, show form
function removeSaveRouteBtn(evt) {
        $('#save-route-btn').attr('style','display:none ;');
        $('#save-form').removeAttr('style');
        $('#save-route-form-btn').removeAttr('style');
};

//------------ SAVE ROUTE FORM ------------\\

// handle drop down form in save route action
let inputBox = document.getElementById('existing-collection-name');
let dropdownList = document.getElementById('dropdown');

dropdownList.onchange = function(){
     inputBox.innerHTML = this.value;
}








//GET ROUTE CALCULATION
$('#calcuate-route-btn').on('click', handleBboxSend);

function handleBboxSend(evt) {
    // start loading gif
    $('.modal').modal('show');
    // hide calculate route button as soon as clicked 
    $('#calcuate-route-btn').attr('style','display:none ;');
    
    let bbox = draw.getAll();

    // add bbox to map 
    map.addSource('bbox', {
        "type": "geojson",
        "data": bbox
        });
    map.addLayer({
        "id": "bbox-geometry",
        "type": "fill",
        "source": "bbox", 
        "paint": {
            'fill-color': '#FFE400',
            'fill-opacity': 0.3,
        }
    }); 

    //remove ability to draw polygon after the bbox polygon is added 
    map.removeControl(draw);

    bbox = JSON.stringify(bbox);

    const formInputs = {
        'bbox_geometry' : bbox
    };
    // send bbox geometry to backend to generate route data 
    // the outout of the get request (route information)
    // is sent as the parameter to addBboxAndRoute
    $.get('/generate_route_data.json', formInputs, addBboxAndRoute);    
}

function addBboxAndRoute(displayGeojsons) {
    // end loading gif
    $('.modal').modal('hide');

    $('#animate-route-btn').removeAttr('style');
    $('#save-route-btn').removeAttr('style');
    $('#save-route-btn').on('click', removeSaveRouteBtn);
    // get geometry feature collections back from get request and 
    // jsonify each

    // let bboxGeometry = JSON.parse(displayGeojsons['bbox_geometry']);
    let edgesGeometry = JSON.parse(displayGeojsons['edges_geometry']);
    let nodesGeometry = JSON.parse(displayGeojsons['nodes_geometry']);
    let routeGeometry = JSON.parse(displayGeojsons['route_geometry']);

    let bboxLineString = turf.lineString(routeGeometry.features[0].geometry.coordinates);

    let turfBox = turf.bbox(bboxLineString);
    let turfbboxPolygon = turf.bboxPolygon(turfBox);
    let coordsList = turfbboxPolygon.geometry.coordinates[0]

    let allX = [] 
    let allY = [] 

    coordsList.forEach((coord) => {
        allX.push(coord[0]);
        allY.push(coord[1]);
    })
    
    let minX =  Math.min.apply(null,allX);
    let minY = Math.min.apply(null,allY);
    let maxX = Math.max.apply(null,allX);
    let maxY = Math.max.apply(null,allY);

    let fitBoundsArray = [[minX, minY] , [maxX, maxY]];
    map.fitBounds(fitBoundsArray, {padding: {
                                    top: 80, 
                                    bottom:100, 
                                    left: 60, 
                                    right: 60}
    });

    $('#animate-route-btn').click({routrgeometry : routeGeometry}, animateRoute);

    // reduce bbox opacity
    map.setPaintProperty('bbox-geometry', 'fill-opacity', .1);


    // POINT 
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
    map.addLayer({
        "id": "point",
        "source": "point",
        "type": "symbol",
        "layout": {
            "icon-image": "person", // CHANGE
            "icon-allow-overlap": true,
            "icon-ignore-placement": true,
            "icon-size": 1.25,
            "icon-anchor" : "bottom"
        }
    });

    // NODES -- add nodes feature collection to map
    map.addSource('nodes', {
        "type": "geojson",
        "data" : nodesGeometry
    });
    
    // add nodes layer as symbol type 
    map.addLayer({
        "id" : "nodes-geometry",
        // "type" : "symbol",
        "type" : "symbol",
        "source" : "nodes",
        "layout": {
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
    // EDGES - add edges feature collection to map
    map.addSource('edges', {
        "type": "geojson",
        "data": edgesGeometry
        });

    map.addLayer({
        "id": "edges-geometry",
        "type": "line",
        "source": "edges", 
        "paint": {
            "line-color" : 'rgba(0,0,205,0.3)',
            "line-width": 3,
            "line-opacity": 1
        }
    }, "nodes-geometry"); // second agument determines which layer should be direcly above the bbox layer

    // ROUTE - add route geometry to be used as animation path later on
    map.addSource('route', {
        "type": "geojson",
        "data": routeGeometry
        });
    map.addLayer({
        "id": "route-geometry", 
        "type": "line",
        "source": "route", 
        "paint": {
            "line-color" : 'rgba(0,0,205,0)',
        }
    });
}

//------------ SAVE ROUTE ------------\\

// send route data to backend on click of save button in form
$('#save-route-form-btn').on('click', handleSaveRoute);

function handleSaveRoute(evt) {
    // get data currently on map to send back for saving 
    const userId = $('#current-user-id').val();
    const nodesData = map.getSource('nodes')._data;
    const bboxData = map.getSource('bbox')._data;
    const edgesData = map.getSource('edges')._data;
    const routeLineData = map.getSource('route')._data;
    const routeLength = routeLineData.features[0].properties.route_length_km

    // if there is no route name given - name NoRouteName
    let  destinationRouteName = $('#route_name').val();
    let destinationCollection = "";

    const newCollectionName = $('#new-collection-name').val(); 
    const existingCollectionName = $('#existing-collection-name').val();

    if (destinationRouteName.length < 1) {
        // destinationRouteName = "NoName";
        alert('Route name required.')
    }

    else {
        // if user selected new collection in the drop down
        // and entered something in the text box 
        // set the destination collection name to 
        if ((existingCollectionName == "New collection") && (newCollectionName.length>0))  {
            alert(`New collection ${newCollectionName} approved!`);
            destinationCollection = newCollectionName;
        } 
        // if user selected something in collection Name other than new ollection and blank
        else if ((existingCollectionName != "New collection") && (existingCollectionName.length > 0)){
            alert(`Existing collection ${existingCollectionName} approved!`);
            destinationCollection = existingCollectionName;
        } else {
            alert('Collection name required.');
        }

    }

    // if a destination collection has been approved, send data to server for saving in db
    if (destinationCollection.length > 0) {
        const formInputs = {
            'user_id' : userId,
            'nodes_data' : JSON.stringify(nodesData),
            'bbox_data' : JSON.stringify(bboxData),
            'edges_data' : JSON.stringify(edgesData),
            'route_line_data': JSON.stringify(routeLineData),
            'destination_collection_name' : JSON.stringify(destinationCollection),
            'new_route_name' : JSON.stringify(destinationRouteName),
            'route_length' : routeLength
          };
        // the outout of the get request (what is returned from the url route)
        // is sent as the parameter to addBboxAndRoute
        $('#save-route-form-btn').attr('style','display:none ;')

        // send post request -> get back confirmation message from backend
        $.post('/save_route.json', formInputs, confirmSavedRoute);
    }
}

function confirmSavedRoute(confirmationMessage){
    $('#save-form').attr('style','display:none ;');  
    const savedRouteName = confirmationMessage['route_name'];
    const savedRouteSuccess = confirmationMessage['success'];
    if (savedRouteSuccess == 'false'){
        alert( savedRouteName + ' could not be saved. Try again.')
    }    
}


//------------ ANIMATION ------------\\

// PLAY ROUTE
function animateRoute(evt){

    // get route geometry from event 
    let route = evt.data.routrgeometry
    // Addsingle point that animates along the route.
    // Coordinates are initially set to the first coordinate in the route
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
    let path = [];

    // Number of steps to use in the path and animation, more steps means
    // a smoother path and animation, but too many steps will result in a
    // low frame rate

    // lower steps = faster movement along route
    const steps = (lineDistance/.004)*1.2

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
        path.push(segment.geometry.coordinates);
    }

    // Update the route with calculated path coordinates
    route.features[0].geometry.coordinates = path;
    // Used to increment the value of the point measurement against the route.
    let counter = 0
    function animate() {
        // Update point geometry to a new position based on counter denoting
        // the index to access the path.

        // what makes the icon move:
        // need to control for the end of the route where you don't want
        // to index outside of the coordinates array
        if (counter < (route.features[0].geometry.coordinates).length) {
            point.features[0].geometry.coordinates = route.features[0].geometry.coordinates[counter];
        } else {
            point.features[0].geometry.coordinates = route.features[0].geometry.coordinates[counter-1];
        }; 
        // Update the source with this new data.
        map.getSource('point').setData(point);
        // Request the next frame of animation so long the end has not been reached.
        if (counter < steps) {
            requestAnimationFrame(animate);
        }
        counter = counter + 1;
    }

    animate(counter);
};

