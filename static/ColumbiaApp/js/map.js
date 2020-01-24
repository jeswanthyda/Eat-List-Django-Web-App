function initAutocomplete() {
    var map = new google.maps.Map(document.getElementById('map'), {
      center: {
        lat: 41.850033,
        lng: -87.6500523
      },
      zoom: 4.5,
      disableDefaultUI:true
    });
    var service = new google.maps.places.PlacesService(map);

    // Create the search box and link it to the UI element.
    var input1 = document.getElementById('location-searchbox');
    var searchBox = new google.maps.places.Autocomplete(input1);
    var input2 = document.getElementById('cuisine-searchbox');
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(input1);
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(input2);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
      searchBox.setBounds(map.getBounds());
    });
    var markers = [];

    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    var button = document.getElementById("submit-search")
    button.addEventListener("click", function() {
        place = searchBox.getPlace();
        var lat = place.geometry.location.lat();
        var lng = place.geometry.location.lng();
        var loc = new google.maps.LatLng(lat, lng);
        var cuisine = input2.value;
        var request = {
            location: loc,
            query: cuisine,
            radius: '500',
            type: ['restaurant']
        };
        service.textSearch(request, function(results,status) {
            if (status == google.maps.places.PlacesServiceStatus.OK) {
                // Clear out the old markers.
                markers.forEach(function(marker) {
                    marker.setMap(null);
                });
                markers = [];
                // For each place, get the location.
                var bounds = new google.maps.LatLngBounds();
                results = rankResults(results);
                results.forEach(function(place) {
                    if(!place.geometry) {
                        console.log("Returned place contains no geometry");
                        return;
                    }
                    
                    image = getIcon(place.color)
                    // Create a marker for each place.
                    markers.push(new google.maps.Marker({
                        map: map,
                        position: place.geometry.location,
                        icon: image
                    }));
                    contentString = "<div class='card' style='max-width: 200px;'>" +
                    "<div class='card-body'>" + 
                      "<h5 class='card-title'>" + place.name + "</h5>" +
                      "<h6 class='card-subtitle mb-2 text-muted'>Rating: " + place.rating + "</h6>" +
                      "<p class='card-text'>Some quick example text to build on the card title and make up the bulk of the card's content.</p>" +
                      "<button onclick=\"add_to_fav(\'"+place.name.replace(/'/g, "\\'")+"',\'"+cuisine.replace(/'/g, "\\'")+"\')\" class='card-link'>Add to Favorites</button>" +
                      "<a href='#' class='card-link'>Website</a>" + "</div>" + "</div>"
                    
                    var marker = markers.slice(-1)[0] 
                    //Info Window for the markers
                    var infowindow = new google.maps.InfoWindow({
                        content: contentString,
                        maxWidth: 500
                    });
                    google.maps.event.addListener(marker, 'click', function() {
                        infowindow.open(map,marker);
                    });

                    if (place.geometry.viewport) {
                        // Only geocodes have viewport
                        bounds.union(place.geometry.viewport);
                    } else {
                        bounds.extend(place.geometry.location);
                    }

                });
                map.fitBounds(bounds);
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", function(event) {
    initAutocomplete();
});

function rankResults(results) {
    for (i = 0; i < results.length; i++) { 
        results[i]['criteria'] = results[i]['rating'];
    } 
    results= sortByKey(results,"criteria");
    for (i = 0; i < results.length; i++) { 
        results[i]['color'] = perc2color(i/results.length*100);
    } 
    return results
}

function sortByKey(array, key) {
    return array.sort(function(a, b) {
        var x = a[key]; var y = b[key];
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}

function perc2color(perc) {
	var r, g, b = 0;
	if(perc < 50) {
		r = 255;
		g = Math.round(5.1 * perc);
	}
	else {
		g = 255;
		r = Math.round(510 - 5.10 * perc);
	}
	var h = r * 0x10000 + g * 0x100 + b * 0x1;
	return '#' + ('000000' + h.toString(16)).slice(-6);
}

function getIcon(color) {
    var pinColor = color;
    var pinLabel = "A";

    // Pick your pin (hole or no hole)
    var pinSVGHole = "M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z";
    var labelOriginHole = new google.maps.Point(12,15);
    var pinSVGFilled = "M 12,2 C 8.1340068,2 5,5.1340068 5,9 c 0,5.25 7,13 7,13 0,0 7,-7.75 7,-13 0,-3.8659932 -3.134007,-7 -7,-7 z";
    var labelOriginFilled =  new google.maps.Point(12,9);


    var markerImage = {  // https://developers.google.com/maps/documentation/javascript/reference/marker#MarkerLabel
        path: pinSVGFilled,
        anchor: new google.maps.Point(12,17),
        fillOpacity: 1,
        fillColor: pinColor,
        strokeWeight: 2,
        strokeColor: "white",
        scale: 2,
        labelOrigin: labelOriginFilled
    };
    return markerImage;
}