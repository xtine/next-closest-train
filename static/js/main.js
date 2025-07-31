// Native JavaScript method to get the user's location.
//
// https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API/Using_the_Geolocation_API#examples
//

function getCurrentLocalTimeHHMMSS() {
  const now = new Date();

  let hours = now.getHours();
  let minutes = now.getMinutes();
  let seconds = now.getSeconds();

  // Pad single digits with a leading zero
  hours = hours < 10 ? '0' + hours : hours;
  minutes = minutes < 10 ? '0' + minutes : minutes;
  seconds = seconds < 10 ? '0' + seconds : seconds;

  // HH:MM:SS for stop_times
  return `${hours}:${minutes}:${seconds}`;
}

function geolocateUser() {
  const status = document.querySelector(".user-location-status");
  const userLocationInfo = document.querySelector(".user-location-info");
  const userLocationStation = document.querySelector(".user-location-station");
  const userLocationLine = document.querySelector(".user-location-line");
  const userStopTimes = document.querySelector(".user-stop-times");

  function success(position) {

    const coordinates = {
      lat: position.coords.latitude,
      lon: position.coords.longitude,
      lat_short: Number((position.coords.latitude).toFixed(2)),
      lon_short: Number((position.coords.longitude).toFixed(2)),
      userTime: getCurrentLocalTimeHHMMSS()
    }

    // hidden input token get CSRF
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    status.style.display = 'none';

    // DEBUG: show user information (coords, time)
    console.log(coordinates)

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
      .then(response => response.json())
      .then(user_station => {
        userLocationInfo.style.display = 'block';

        // DEBUG: show user's closest station
        console.log(user_station)

        userLocationStation.textContent = user_station.stop_name;

        userLocationLine.textContent = user_station.parent_station

        const stop_times = user_station.stop_times

        stop_times.forEach(stop => {
          const listItem = document.createElement('li'); // Create a new <li> element

          // Set the content of the list item
          listItem.textContent = `${stop.departure_time} - ${stop.stop_headsign}`;

          userStopTimes.appendChild(listItem)
        });

      })

  }

  function error() {
    status.style.display = 'block';
    status.textContent = "Unfortunately, we were not able to retrieve your location.";
  }

  if (!navigator.geolocation) {
    status.style.display = 'block';
    status.textContent = "Geolocation is not supported by your browser.";
  } else {
    status.style.display = 'block';
    status.textContent = "Locating...";
    navigator.geolocation.getCurrentPosition(success, error);
  }
}

document.querySelector("#user-location").addEventListener("click", geolocateUser);