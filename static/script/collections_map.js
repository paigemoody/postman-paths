mapboxgl.accessToken = 'pk.eyJ1IjoicGFpZ2VlbW9vZHkiLCJhIjoiY2owbDcyejhvMDJwNzJ5cDR0YXE1aG10MCJ9.a-JLnrmMPSJNwOGQdloTDA';
var map = new mapboxgl.Map({
    container: 'map', // container id
    style: 'mapbox://styles/paigeemoody/cjwjzqywq2orj1dqqvdvwchhm',
    center: [-122.453554,37.762436], // starting position [lng, lat]
    zoom: 10 // starting zoom
});


map.on("load", function() {

    const route_ids = [1,2,3]

    route_ids.forEach(route_id => {

        // POINT FOR ANIMATION
        const id = route_id;

        animationId = `point${id}`
        animationSource = `/collections/get_route_data/${id}/animate_point_geometry.json`
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
        //NODES
        nodesId = `nodes${id}`
        nodesSource = `collections/get_route_data/${id}/nodes_geometry.json`
        nodesLayerId = `nodes${id}`

        map.addSource(nodesId, {
            "type": "geojson",
            "data" : nodesSource
        });

        map.addLayer({
            "id" : nodesLayerId,
            // "type" : "symbol",
            "type" : "symbol",
            "source" : nodesId,
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
        }, animationId); // add point layer order ref 

        // EDGES
        edgesId = `edges${id}`
        edgesSource = `collections/get_route_data/${id}/edges_geometry.json`
        edgesLayerId = `edges${id}`

        map.addSource(edgesId, { //  bbox in this case is a variable that is a feature collection
            "type": "geojson",
            "data": edgesSource
            });

        map.addLayer({
            "id": edgesLayerId, // rename?
            "type": "line",
            "source": edgesId, 
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
        }, nodesId);

        // ROUTE GEOM FOR ANIMATION
        edgesId = `route${id}`
        edgesSource = `collections/get_route_data/${id}/route_geometry.json`
        edgesLayerId = `route${id}`

        map.addSource(edgesId, { //  bbox in this case is a variable that is a feature collection
            "type": "geojson",
            "data": edgesSource
            });

        map.addLayer({
            "id": edgesLayerId, // rename?
            "type": "line",
            "source": edgesId, 
            "paint": {
                "line-color" : 'rgba(0,0,205,0)',
            }
        });    


    })

});