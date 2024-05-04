# Import the dependencies.
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)
# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create a session
#session = Session(engine)

#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"  # Using HTML entities for < and >
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"  # Using HTML entities for < and >
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Find the most recent date in the data set.
    latest_date_result = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    if latest_date_result:
        latest_date = latest_date_result[0]
        # Calculate the date one year ago from the last data point in the database
        # one_year_ago = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)
        max_date = session.query(func.max(Measurement.date)).scalar()
        one_year_ago = session.query(func.date(max_date, '-1 year')).scalar()

        # Perform a query to retrieve the data and precipitation scores
        results = session.query(Measurement.date, Measurement.prcp) \
            .filter(Measurement.date >= one_year_ago) \
            .all()

        # Query all passengers
        # results = session.query(Measurement.date, Measurement.prcp).all()

        session.close()
        # Create a dictionary from the row data and append to a list of all precipitation
        all_precipitation = []
        for date, prcp in results:
            precipitation_dict = {}
            if prcp is not None:  # This line ensures we do not include days with null precipitation data.
                precipitation_dict[date] = prcp
                all_precipitation.append(precipitation_dict)

        return jsonify(all_precipitation)
    else:
        session.close()
        return jsonify({"error": "No precipitation data found"}), 404

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Stations data including all parameter each station"""
    # Query all passengers
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude).all()

    session.close()

    # Create a list of dictionaries to hold each station's data
    all_stations = []
    for id, station, name, latitude, longitude in results:
        station_dict = {
            "id": id,
            "station": station,
            "name": name,
            "latitude": latitude,
            "longitude": longitude
        }
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to find the most active station
    most_active_station = session.query(Measurement.station, func.count(Measurement.tobs)) \
        .group_by(Measurement.station) \
        .order_by(func.count(Measurement.tobs).desc()) \
        .first()[0]

    # Query to find the last date in the database for the most active station
    last_date = session.query(Measurement.date) \
        .filter(Measurement.station == most_active_station) \
        .order_by(Measurement.date.desc()) \
        .first()[0]

    # Convert last date to datetime object to calculate the date one year ago
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    # Query the last year of temperature observations for the most active station
    results = session.query(Measurement.date, Measurement.tobs) \
        .filter(Measurement.station == most_active_station) \
        .filter(Measurement.date >= one_year_ago) \
        .all()

    session.close()

    # Create a list of dictionaries for each temperature observation
    temperature_observations = [{"date": date, "tobs": tobs} for date, tobs in results]

    return jsonify(temperature_observations)

@app.route("/api/v1.0/<start>")
def stats_from_start(start):
    session = Session(engine)
    """Return TMIN, TAVG, and TMAX for all dates that are greater or equal the start date."""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                     .filter(Measurement.date >= start).all()
    session.close()

    # Unpack the result tuple
    tmin, tavg, tmax = results[0]
    temp_data = {
        "TMIN": tmin,
        "TAVG": tavg,
        "TMAX": tmax
    }
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def stats_from_start_to_end(start, end):
    session = Session(engine)
    """Return TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                     .filter(Measurement.date >= start)\
                     .filter(Measurement.date <= end).all()
    session.close()

    # Unpack the result tuple
    tmin, tavg, tmax = results[0]
    temp_data = {
        "TMIN": tmin,
        "TAVG": tavg,
        "TMAX": tmax
    }
    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)