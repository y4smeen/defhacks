from flask import Flask, render_template, request

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
        return render_template( "results.html", city=city, state=state, near=nearlist, price=price )

@app.route( "/about" )
def about():
    return render_template( "about.html" )    

if __name__ == "__main__":

    app.debug = True
    app.run()
