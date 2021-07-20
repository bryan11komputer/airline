import csv

from config import Config

from flask import Flask, render_template, request
from models import *

thisConfig = Config()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = thisConfig.DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
	file = open("flights.csv")
	csv_reader = csv.reader(file)
	for origin, destination, duration in csv_reader:
		flight = Flight(origin=origin, destination=destination, duration=duration)
		db.session.add(flight)
		print(f"Added flight from {origin} to {destination}, lasting {duration} minute(s)")
	db.session.commit()

if __name__ == '__main__':
	with app.app_context():
		main()