from flask import Flask, render_template, request
import urllib2, urllib, json,time

key = "AIzaSyAcXE_nj31Hrj5EEhBz3vAXluEZ4ox-pLk"
#token = "bMAwaXXybvZyuuRPNoNv"
nextPage = ""
app = Flask(__name__)

@app.route( "/", methods = ["GET", "POST"] )
def form():
    if request.method == "GET":
        return render_template( "form.html" )
    else:
        city = request.form["city"]
        #state = request.form["state"]
        near = request.form["near"]
        nearlist = near.split(",")
        #price = request.form["price"]
        cityState = city
        latLong = geo_loc(cityState)
        place =  findPlaces(latLong,nearlist)
        buy = findBuyPrice(place)
        rent = findRentPrice(place)
        return render_template( "results.html", place=place, buy=buy, rent=rent, nearlist=near )

@app.route( "/about" )
def about():
    return render_template( "about.html" )

def geo_loc(location):
#finds the longitude and latitude of a given location parameter using Google's Geocode API
#return format is a dictionary with longitude and latitude as key
    loc = urllib.quote_plus(location)
    googleurl = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (loc,key)
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
    zipcode = []
    for keyword in nearlist:
        ltemp = []
        googleurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&key=%s&radius=2000&keyword=%s" % (latLong,key,keyword)
        request = urllib2.urlopen(googleurl)
        results = request.read()
        gd = json.loads(results) #dictionary
        ltemp = findFirst100(gd,latLong,keyword)
        for address in ltemp:
            placeurl = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (address,key)
            request = urllib2.urlopen(placeurl)
            results = request.read()
            gd1 = json.loads(results) #dictionary
            shortzip = ""
            try:
                shortzip = gd1['results'][0]['address_components'][8]['long_name']
                zipcode.append(shortzip)
            except:
                print "bad: " + address
        l.append(ltemp)
    #print zipcode
    return findMost(zipcode);

def findMost(zipcode):
    count = 0;
    savecount = 0;
    saveme = 0;
    x = 0
    for i in zipcode:
        while (x < len(zipcode)):
            for x in zipcode:
                if i == x:
                    count+=1;
                    zipcode.remove(i)
            if count > savecount:
                saveme = i
            count = 0
        x = 0
    return saveme

def findFirst100(dict,latLong,keyword):
    ltemp = []
    for place in dict['results']:
        ltemp.append(str(place['geometry']['location']['lat']) + "," + str(place['geometry']['location']['lng']))
    try:
        nextPage = dict['next_page_token']
    except:
        print "PAGE NOT FOUND 1"
    for i in range(4):
        try:
            ltemp += findNext20(nextPage,latLong,keyword)
        except:
            break
    return ltemp

def findNext20(token,latLong,keyword):
    ltemp1 = []
    googleurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=%s&key=%s" % (token,key)
    time.sleep(2)
    request = urllib2.urlopen(googleurl)
    results = request.read()
    gd = json.loads(results) #dictionary
    try:
        nextPage = gd['next_page_token']
    except:
        print "PAGE NOT FOUND 2"
    for place in gd['results']:
        ltemp1.append(str(place['geometry']['location']['lat']) + "," + str(place['geometry']['location']['lng']))
    return ltemp1

def findRentPrice(zipcode):
    renturl = "https://www.quandl.com/api/v1/datasets/ZILLOW/RZIP_MEDIANRENTALPRICE_ALLHOMES_%s.json" % (zipcode)
    gd2 = 0
    avgrent = -1
    try:
        gd2 = json.loads(urllib2.urlopen(renturl).read())
        avgrent = gd2['data'][0][1]
        print "Rent: $" + str(avgrent)
    except:
        print "Rent Not Available"
    return findPriceHelper(avgrent)

def findPriceHelper(price):
    if (price == -1):
        return "N/A"
    else:
        return str(price)

def findBuyPrice(zipcode):
    buyurl = "https://www.quandl.com/api/v1/datasets/ZILLOW/MZIP_MEDIANSOLDPRICE_ALLHOMES_%s.json" % (zipcode)
    gd1 = 0
    avgbuy = -1
    try:
        gd1 = json.loads(urllib2.urlopen(buyurl).read())
        avgbuy = gd1['data'][0][1]
        print "Buy: $" + avgbuy
    except:
        print "BUY n/a"
    return findPriceHelper(avgbuy)

    

if __name__ == "__main__":

    app.debug = True
    app.run()
