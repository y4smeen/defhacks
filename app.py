from flask import Flask, render_template, request

app = Flask(__name__)

@app.route( "/" )
def index():
    return render_template( "base.html")

@app.route( "/robots" )
def robots():
    return render_template( "form.html" )

@app.route( "/form", methods = ["GET", "POST"] )
def form():
    if request.method == "GET":
        return "pls get here from the form"
    else:
        n = request.form["name"]
        return "Hello "+ n

if __name__ == "__main__":

    app.debug = True
    app.run()
