# Where's my closest LA Metro Rail?
A handy way to find your closest rail station.

Using data from [GTFS Rail](https://gitlab.com/LACMTA/gtfs_rail).

## Why This Project?
Typically I would load up Google Maps to find departure times for Metro Rail stations, however I would still need to search or click the station on the map. This project would be a one click experience without having to open the Maps app.

### Tech Stack
Django/Python, as its my most comfortable platform in develop in. Since I'm not making a highly interactive app, I don't need React or that other nonsense, vanilla CSS keeps it simple and efficient. Building on top of USWDS CSS for a simple design and style foundation gives me all I need presentation wise.

### Transit Data Access
My first idea was to see if Metro API could provide me with the data I needed. However, it couldn't quite figure out how to get stops. Even exploring route ids for rail lines, I couldn't get the stops endpoint to get me what I needed. So I continued to dig.

I then found the GTFS Rail static data, as I don't have access to Swiftly (Google form request for API access? I couldn't rely to get it on time). As I am new to accessing public data transit data, it was an interesting basic dive into all GTFS entails. Quite a lot! Considering the data I need for the first iteration is basic (just rail station metadata and timetables), I figure I could just mock it by importing the data into fixtures. As this is a demo project and not intended for production (yet), SQLite would suffice.

### Technical Journey
It's been a while since I developed an end to end demo app, so I decided to start from scratch. Developing on a Mac, my foundations to start were:
- Update OS X to latest version (Sequoia)
  - Needed so I can get the latest XCode
- Set up zsh files and VS Code
- Install Homebrew, Python (version 3, a surprise since OS X doesn't package Python out of the box anymore), Node, Docker

A pleasant surprise to see how much of my knowledge of Django/Python development has fundamentally stayed the same. It's still pip, virtual environments, and gunicorn. A few things have been spruced up like small touches in the admin interface, more form widgets, slightly better documentation. But the simplicity and ease of shipping a web app through Django has continued to spark joy, especially given how stable it has been throughout the years.

### Agile Development
Step by step, always shipping a MVP:
- Get environment set up
- Local Hello World
  - Set basic templates and styles
  - Show Rail Station information
  - Functional button to find current location
  - Import GTFS data into database via fixtures
  - Backend endpoint(s) to fetch data:
    - `closestStation` - nearest neighbor to user's coordinates vs all station coordinates to return the nearest station
  - Button will now show closest station to user location
  - Fall back for button, if can't locate data, enter address to find coordinates
  - Endpoint: `departureTimes` - returns next departure times for the nearest station, after current time.
- Dockerize and deploy

### Blue Skies
Ideally, I'd like to get real time data so I can make a one-click version of the [Metro Arrivals](https://www.metro.net/riding/nextrip/) page. But for this demo app, fixed data suffices for presentation purposes.