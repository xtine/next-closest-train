// Simple native JavaScript function to get the user's location.
//
// https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API/Using_the_Geolocation_API#examples
//

function geolocateUser() {
  const status = document.querySelector("#user-location-status");
  const mapLink = document.querySelector("#map-link");

  mapLink.href = "";
  mapLink.textContent = "";

  function success(position) {

    const coordinates = {
        lat: position.coords.latitude,
        lon: position.coords.longitude,
        lat_short: Number((position.coords.latitude).toFixed(2)),
        lon_short: Number((position.coords.longitude).toFixed(2))
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    status.textContent = "";

    mapLink.href = `https://www.openstreetmap.org/#map=18/${coordinates.lat}/${coordinates.lon}`;

    mapLink.textContent = `Your coordinates: ${coordinates.lat_short} °, ${coordinates.lon_short} °`;

    // send coordinates to view to grab nearest station
    // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
    //
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(coordinates)
    })
  }

  function error() {
    status.textContent = "Unable to retrieve your location";
  }

  if (!navigator.geolocation) {
    status.textContent = "Geolocation is not supported by your browser";
  } else {
    status.textContent = "Locating…";
    navigator.geolocation.getCurrentPosition(success, error);
  }
}

document.querySelector("#user-location").addEventListener("click", geolocateUser);