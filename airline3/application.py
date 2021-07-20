import os
 
from config import Config
 
from flask import Flask, render_template, request
from models import *
 
 
thisConfig = Config()
 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = thisConfig.DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
 
 
@app.route("/")
def index():
    # QUERY = "SELECT * FROM flights;"
    # flights = db.execute(QUERY).fetchall()
    flights = Flight.query.all()
 
    return render_template("index.html", flights=flights)
 
@app.route("/book", methods=["POST"])
def book():
 
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError as e:
        return render_template("error.html", message=f"Invalid flight number.\nError : {e}")
 
    #make sure the flight exists
    # QUERY = "SELECT * FROM flights WHERE id = :id;"
    # exists = db.execute(QUERY,{"id":flight_id}).rowcount
    flight = Flight.query.get(flight_id)
 
 
    if flight == 0: #exists
        return render_template("error.html", message=f"No such flight with that id.")
    else:
        # QUERY = "INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id);"
        # db.execute(QUERY,{"name":name, "flight_id":flight_id})
        # db.commit()
        passenger = Passenger(name=name, flight_id=flight_id)
        print(passenger.name, passenger.flight_id)
        db.session.add(passenger)
        db.session.commit()
        return render_template("success.html")
    
@app.route("/flights")
def flights():
    # lists all flights and their details link
    # QUERY = "SELECT * FROM flights;"
    # flights = db.execute(QUERY).fetchall()
    flights = Flight.query.all()
 
    return render_template("flights.html", flights=flights)
 
@app.route("/flight/<int:flight_id>")
def flight(flight_id):
    # make sure flight exists
    # QUERY = "SELECT * FROM flights WHERE id = :id;"
    # flight = db.execute(QUERY,{"id":flight_id}).fetchone()
    flight = Flight.query.get(flight_id)
    if flight is None :
        return render_template("error.html", message="No such flight.")
    else:
        #get all passengers
        # QUERY = "SELECT * FROM passengers WHERE flight_id = :flight_id;"
        # passengers = db.execute(QUERY, {"flight_id":flight_id}).fetchall()
        passengers = Passenger.query.filter_by(flight_id = flight_id).all()
        for passenger in passengers:
            print(passenger.name, passenger.flight_id)
        return render_template("flight.html", flight=flight, passengers=passengers)
