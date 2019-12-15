import urllib.request, json, math


def findcoor(lat, lon, distance, bearing):
    # print("Finding Coordinate:")
    brng = (bearing*math.pi)/180  # Bearing is 90 degrees converted to radians.
    d = distance # Distance in km

    lat1 = math.radians(lat)  # Current lat point converted to radians
    lon1 = math.radians(lon)  # Current long point converted to radians

    lat2 = math.asin(math.sin(lat1)*math.cos(d/6378.1) +
         math.cos(lat1)*math.sin(d/6378.1)*math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/6378.1)*math.cos(lat1),
                 math.cos(d/6378.1)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    return lat2, lon2


def geocode(current):
    current = current.replace(' ', '+')
    endpoint = 'https://maps.googleapis.com/maps/api/geocode/json?'
    api_key = 'AIzaSyBTcJcpE8loo8Hmel4kVw5hXa8VOv2FLoo'
    nav_request = 'address={}&key={}'.format(current, api_key)
    request = endpoint+nav_request
    response = urllib.request.urlopen(request).read()
    geocode = json.loads(response)
    return [geocode['results'][0]['geometry']['location']['lat'],
            geocode['results'][0]['geometry']['location']['lng']]


def getlegs(lat1, lon1, lat2, lon2):
    # print("Getting Distance:")
    coor1 = str(lat1)+','+str(lon1)
    coor2 = str(lat2)+','+str(lon2)
    # print(coor1)
    # print(coor2)
    # Google MapsDdirections API endpoint
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'AIzaSyBTcJcpE8loo8Hmel4kVw5hXa8VOv2FLoo'
    # Asks the user to input Where they are and where they want to go.
    origin = coor1.replace(' ', '+')
    destination = coor2.replace(' ', '+')
    # Building the URL for the request
    nav_request = 'origin={}&destination={}&mode={}&key={}'.format(origin, destination, 'walking', api_key)
    request = endpoint + nav_request
    # Sends the request and reads the response.
    response = urllib.request.urlopen(request).read()
    # Loads response as JSON
    directions = json.loads(response)
    # print(directions['routes'][0]['legs'][0]['distance']['text'])
    # print(directions['routes'][0]['legs'])
    # 43.2569615,-79.9095541
    # 43.2615183,-79.9150966
    return directions['routes'][0]['legs'][0]


def findangle(r, dist):
    # print("Finding Anlge:")
    angle = math.acos((2*(r*r)-(dist*dist))/(2*r))
    # print()
    return angle


# prints walking directions to the python console
def getinstructions(leg):
    coorinstructions = [[leg['start_location']['lat'], leg['start_location']['lng']]]
    bad_chars = '<b></b>'
    for step in leg['steps']:
        skip = False
        curr = ""
        for char in step['html_instructions']:
            if char == '<':
                skip = True
            if not skip:
                curr += char
            if char == '>':
                skip = False
                curr += " "
        print(curr)

        coorinstructions.append([step['end_location']['lat'], step['end_location']['lng']])

    return coorinstructions

"""
def visualize(location):
    import requests, webbrowser
    endpoint = 'https://maps.googleapis.com/maps/api/staticmap?'
    api_key = 'AIzaSyBTcJcpE8loo8Hmel4kVw5hXa8VOv2FLoo'
    location = location.replace(' ', '+')
    center = location
    zoom = 17
    r = requests.get(endpoint+"center="+center+"&zoom="+str(zoom)+"&size=2560x1440&key="+api_key)
    print(endpoint+"center="+center+"&zoom="+str(zoom)+"&size=2560x1440&key="+api_key)
    webbrowser.open(endpoint+"center="+center+"&zoom="+str(zoom)+"&size=2560x1440&key="+api_key)
"""


# creates a rough visualization of the walking path
# and saves it to "C:\\Users\\user\\Desktop\\map11.html"
def visualize(lats, lons, slats, slons):
    import gmplot, webbrowser
    # GoogleMapPlotter return Map object
    # Pass the center latitude and
    # center longitude

    gmap = gmplot.GoogleMapPlotter(lats[0], lons[1], 13)
    gmap.plot(lats, lons, 'cornflowerblue', edge_width=10)
    gmap.scatter(slats, slons, '# FF0000', size=9, marker=False)
    # ^black circle things
    gmap.marker(slats[0], slons[0], title='START')

    gmap.apikey = 'AIzaSyBTcJcpE8loo8Hmel4kVw5hXa8VOv2FLoo'
    # Pass the absolute path
    gmap.draw("C:\\Users\\darks\\Desktop\\map11.html")


lat1, lon1 = geocode(input())
perimeter = int(input())
r = perimeter/3
lat2, lon2 = findcoor(lat1, lon1, r, 0)  # degrees
angle = findangle(r, r)
lat3, lon3 = findcoor(lat1, lon1, r, angle)  # degrees

legs1 = getlegs(lat1, lon1, lat2, lon2)
legs2 = getlegs(lat2, lon2, lat3, lon3)
legs3 = getlegs(lat3, lon3, lat1, lon1)

legs1 = getinstructions(legs1)
legs2 = getinstructions(legs2)
legs3 = getinstructions(legs3)

lats = [j for i in [[y[0] for y in x] for x in [legs1, legs2, legs3]] for j in i]
lons = [j for i in [[y[1] for y in x] for x in [legs1, legs2, legs3]] for j in i]
visualize(lats, lons, [legs1[0][0], legs2[0][0], legs3[0][0]], [legs1[0][1], legs2[0][1], legs3[0][1]])
