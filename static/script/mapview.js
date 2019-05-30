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

// RENDER BBOX as new source? 
    


//GET ROUTE CALCULATION

function addBboxAndRoute(displayGeojsons) {

    // remove draw function 
    // map.removeControl(draw);

    // hide calculate route button
    $('#calcuate-route-btn').attr('style','display:none ;');
    
    // get geometry feature collections back from get request and 
    // jsonify each

    // let bboxGeometry = JSON.parse(displayGeojsons['bbox_geometry']);
    let edgesGeometry = JSON.parse(displayGeojsons['edges_geometry']);
    let nodesGeometry = JSON.parse(displayGeojsons['nodes_geometry']);

    // reduce bbox opacity
    map.setPaintProperty('bbox-geometry', 'fill-opacity', .1);

    // console.log("\n\ntype bbox geom:", typeof bboxGeometry);
    // console.log("\n\ntype edges geom:", typeof edgesGeometry);
    

    console.log("\n\n\n nodes geometry", nodesGeometry)
    console.log("\n\n\n edges geometry", edgesGeometry)


    // console.log("\n\n\n start node", nodesGeometry['features'][0]['properties']['start_node'])

    // console.log("\n\n\n start node type", (typeof nodesGeometry['features'][0]['properties']['start_node']))
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
    });


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
