mapboxgl.accessToken = 'pk.eyJ1IjoicGFpZ2VlbW9vZHkiLCJhIjoiY2owbDcyejhvMDJwNzJ5cDR0YXE1aG10MCJ9.a-JLnrmMPSJNwOGQdloTDA';
var map = new mapboxgl.Map({
    container: 'map', // container id
    style: 'mapbox://styles/paigeemoody/cjwjzqywq2orj1dqqvdvwchhm',
    center: [-122.453554,37.762436], // starting position [lng, lat]
    zoom: 10 // starting zoom
});


map.on("load", function() {

    // POINT FOR ANIMATION
    const id = 1;
    animationId = `point${id}`
    animationSource = `http://0.0.0.0:5001/collections/get_route_data/${id}/animate_point_geometry.json`
    animationLayerId = `point${id}`

    map.addSource(animationId, {
        "type": "geojson",
        "data": animationSource
    });
    // add point to be animated to graph 
    map.addLayer({
        "id": animationLayerId,
        "source": animationId,
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

    // NODES
    // map.addSource("nodes", {
    //     "type": "geojson",
    //     "data" : 'http://0.0.0.0:5001/collections/get_route_data/1/nodes_geometry.json'
    // });

    // map.addLayer({
    //     "id" : "nodes-geometry",
    //     // "type" : "symbol",
    //     "type" : "symbol",
    //     "source" : "nodes",
    //     "layout": {
    //         "text-field": "{visit_order}",
    //         "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
    //         "text-offset": [0, 0.6],
    //         "text-anchor": "top"
    //         },
    //     paint: {
    //         "text-color": "#000000",
    //         "text-halo-color": "#ffffff",
    //         "text-halo-width": 1
    //       }
    // }, "point"); // add point layer order ref 

    // // EDGES
    // map.addSource('edges', { //  bbox in this case is a variable that is a feature collection
    //     "type": "geojson",
    //     "data": 'http://0.0.0.0:5001/collections/get_route_data/1/edges_geometry.json'
    //     });

    // map.addLayer({
    //     "id": "edges-geometry", // rename?
    //     "type": "line",
    //     "source": "edges", 
    //     "paint": {
    //         // set line color based on number of traversals, to highlight which streets to 
    //         // traverse twice
    //         "line-color" : [
    //             'match',
    //             ['get', 'num_traversals'],
    //             1, 'rgba(0,0,205,0.3)', 
    //             // 1, '#e55e5e', // pink
    //             // 2, '#fbb03b', // orange
    //             2, 'rgba(0,0,205,0.6)',
    //             // 3, '#00FF00', // green
    //             3, 'rgba(0,0,205,0.9)',
    //             'rgba(0,0,205,1)',
    //             // '#123c69' // blue
    //         ],
    //         "line-width": 8,
    //         "line-opacity": 1
    //     }
    // }, "nodes-geometry");

    // // ROUTE GEOM FOR ANIMATION
    // map.addSource('route', { //  bbox in this case is a variable that is a feature collection
    //     "type": "geojson",
    //     "data": 'http://0.0.0.0:5001/collections/get_route_data/1/route_geometry.json'
    //     });

    // map.addLayer({
    //     "id": "route-geometry", // rename?
    //     "type": "line",
    //     "source": "route", 
    //     "paint": {
    //         "line-color" : 'rgba(0,0,205,0)',
    //     }
    // });                                 

});