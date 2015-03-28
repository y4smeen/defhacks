from flask import Flask, render_template, request
import urllib2, urllib, json

key = "AIzaSyDUiZxaQHftGIZ8CgOdF-V24EP1FLt4N1E"
url = ""

app = Flask(__name__)

# @app.route( "/" )
# def index():
#     return render_template( "base.html")

# @app.route( "/search" )
# def robots():

@app.route( "/", methods = ["GET", "POST"] )
def form():
    if request.method == "GET":
        return render_template( "form.html" )
    else:
        city = request.form["city"]
        state = request.form["state"]
        near = request.form["near"]
        nearlist = near.split(",")
        price = request.form["price"]
        cityState = city + ", " + state
        latLong = geo_loc(cityState)
        print findPlaces(latLong,nearlist)
        return render_template( "results.html", loc = latLong, near=nearlist, price=price )

@app.route( "/about" )
def about():
    return render_template( "about.html" )    

def geo_loc(location):
#finds the longitude and latitude of a given location parameter using Google's Geocode API
#return format is a dictionary with longitude and latitude as key
    loc = urllib.quote_plus(location)
    googleurl = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (loc,key)
    print googleurl
    request = urllib2.urlopen(googleurl)
    results = request.read()
    gd = json.loads(results) #dictionary
    result_dic = gd['results'][0] #dictionary which is the first element in the results list
    geometry = result_dic['geometry'] #geometry is another dictionary
    loc = geometry['location'] #yet another dictionary
    retstr = str(loc["lat"])+","+str(loc["lng"])
    return retstr

def findPlaces(latLong,nearlist):
    l = []
    for keyword in nearlist:
        ltemp = []
        googleurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&key=%s&radius=1000&keyword=%s" % (latLong,key,keyword)
        print googleurl
        request = urllib2.urlopen(googleurl)
        results = request.read()
        gd = json.loads(results) #dictionary
        for place in gd['results']:
            ltemp.append(place['vicinity'])
        l.append(ltemp)
    return l
        




if __name__ == "__main__":

    app.debug = True
    app.run()
