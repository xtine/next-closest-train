# Where's my closest LA Metro Rail?
A handy way to find your closest rail station.

Using data collected from [Metro API](https://api.metro.net/docs) and [GTFS Rail](https://gitlab.com/LACMTA/gtfs_rail).

## How to Run
In base directory, create a Python virtual environment
```
python -m venv myenv
```
You can subsitute "myenv" for any name you choose.

Activate the virtual enviroment
```
source myenv/bin/activate
```
Install all requirements of the project using pip:
```
pip install -r requirements.txt
```
Load database and fixtures
```
python manage.py migrate
python manage.py loaddata rail/fixtures/*.json
```
Make sure you set environment variables for your local environment:
```
export DJANGO_SECRET_KEY=set-a-long=and=secure-secret-key-phrase-here

export DEBUG=True

export DJANGO_LOGLEVEL=DEBUG
```
Test files
```
python manage.py test
```
Run the server
```
python manage.py runserver
```

Ideally, I would run this as a contained Docker image, but I couldn't get static files to load, so for now local development is through the local virtual env and django server.

## Why This Project?
Typically I would load up Google Maps to find departure times for Metro Rail stations, however I would still need to search or click the station on the map. This project would be a one click experience without having to open the Google Maps app on my phone.

### Tech Stack
Django/Python, as its my most comfortable platform in develop in. I wish to keep this project as simple and efficient as possible, so I am not relying on front end build scripts or a JavaScript framework. Instead, using native JavaScript as well as vanilla css, but leveraging USWDS CSS for unified presentation styling.

### Transit Data Access
My first idea was to see if Metro API could provide me with the data I needed. However, it couldn't quite figure out how to get stops as the documentation was not enough for me to understand `route_code`. Even exploring route ids for rail lines, I couldn't get the stops endpoint to get me what I needed. So I continued to dig.

I then found the GTFS Rail static data, as I don't have access to Swiftly (Google form request for API access? I couldn't rely to get it on time). As I am new to accessing public data transit data, it was an interesting basic dive into all GTFS entails. Quite a lot! Considering the data I need for the first iteration is basic (just rail station metadata and timetables), I figure I could just mock it by importing the data into fixtures. As this is a demo project and not intended for production (yet), SQLite would suffice.

### Metro Data Fixtures
**Rail Lines**<br>
For the rail lines, I took data from the `https://api.metro.net/LACMTA_Rail/route_overview` endpoint and saved it as a fixture (`rail/fixtures/rail_lines.json`). I notice this data is slightly outdated as it still links to timetables before the Regional Connector was finished. However, it had more data than the GTFS data.

**Rail Stations and Stop Times**<br>
For the `stations.json` and `stop_times.json` fixtures, I loaded data from the GTFS static data, which updates stop times daily. Ideally, I would like to access this data directly as an external API especially if it could give me live data. However with this limitation, I downloaded the raw CSV and translated into Django fixture appropriate json to load.

### Technical Journey
It's been a while since I developed an end to end demo app, so I decided to start from scratch. Developing on a Mac, my foundations to start were:
- Update OS X to latest version (Sequoia)
  - Needed so I can get the latest XCode
- Set up zsh files and VS Code
- Install Homebrew, Python (version 3, a surprise since OS X doesn't package Python out of the box anymore), Node, Docker

A pleasant surprise to see how much of my knowledge of Django/Python development has fundamentally stayed the same. It's still pip, virtual environments, and gunicorn. A few things have been spruced up like small touches in the admin interface, more form widgets, slightly better documentation. But the simplicity and ease of shipping a web app through Django has continued to spark joy, especially given how stable it has been throughout the years.

### Agile Development
I like to develop in an agile fashion, always progressing with interable demos step by step.
- Get environment set up
- "Hello World" - the page loads with templates and styles.
- Import Metro API and GTFS data through fixtures so they are loaded into the database.
- Page showing Metro Rail information (accessing `rail_lines.json` data)
- Functional button to find current location (user can click to view their current coordinates)
- Button will now show closest station to user location ("as crow flies")

### Future Iterations
Ideally, these are also the other considerations and enhancements for the app:
- More substational Python/Django unit tests
- JavaScript unit tests
- PlayWright tests (regression tests)
- Fallback for user location
  - If user's location cannot be found or an error occurs, give them an option to enter their address via text input. (Would also need to santize input and give fallbacks if user supplied address does not work.)
- Currently, the nearest station is shown "as crow flies" shortest distance to user. This doesn't account for walking or car travel time, as another station may be quicker via car/bike/foot. First idea to investigate would be to use Google Maps API to calculate directional times to the X "closest" stations.
- Update Dockerfile to use nginx to serve static files (currently the image works but cannot access static img/js/css files)
- Set up Github actions to deploy the latest Docker image into a dev/staging environment
  - Set up a host instance for CI/CD deployment on a cloud platform


### Blue Skies
Ideally, I'd like to get real time data so I can make a one-click version of the [Metro Arrivals](https://www.metro.net/riding/nextrip/) page. But for this demo app, fixed data suffices for presentation purposes.