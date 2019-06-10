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

        // call your awesome function here
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
            // POINT FOR ANIMATION
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
