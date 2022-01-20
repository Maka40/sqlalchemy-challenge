import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    most_recent_date = dt.date(2017, 8, 23)
    one_year_before = most_recent_date - dt.timedelta(days=365)

    results = session.query(Measurement.prcp, Measurement.date)\
        .filter(Measurement.date < most_recent_date)\
        .filter(Measurement.date >= one_year_before).all()
    
    one_yr_prcp = []
    for result in results:
        prcp_dict = {}
        prcp_dict[result.date] = result.prcp
        one_yr_prcp.append(prcp_dict)
        
    return jsonify(one_yr_prcp)

@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Station.station).all()
    
    all_stations = []
    for result in results:
        stations_dict = {}
        stations_dict["station"] = result.station
        all_stations.append(stations_dict)
        
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    most_recent_date = dt.date(2017, 8, 23)
    one_year_before = most_recent_date - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.station, Measurement.tobs)\
        .filter(Measurement.date < most_recent_date)\
        .filter(Measurement.date >= one_year_before).all()
    
    tobs_results = []
    for result in results:
        tobs_dict = {}
        tobs_dict["date"] = result.date
        tobs_dict["station"] = result.station
        tobs_dict["tobs"] = result.tobs
        tobs_results.append(tobs_dict)
        
    return jsonify(tobs_results)

@app.route("/api/v1.0/<start>")
def start(start, end = ""):
    
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
                            .filter(Measurement.date >= start).all()
    
    min_max_avg = []
    for stat in results:
        min_max_avg_dict = {}
        min_max_avg_dict["Lowest Temp"] = stat[0]
        min_max_avg_dict["Highest Temp"] = stat[1]
        min_max_avg_dict["Average Temp"] = stat[2]
        min_max_avg.append(min_max_avg_dict)
        
    return jsonify(min_max_avg)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end).all()
    
    min_max_avg = []
    for stat in results:
        min_max_avg_dict = {}
        min_max_avg_dict["Lowest Temp"] = stat[0]
        min_max_avg_dict["Highest Temp"] = stat[1]
        min_max_avg_dict["Average Temp"] = stat[2]
        min_max_avg.append(min_max_avg_dict)
        
    return jsonify(min_max_avg)

if __name__ == '__main__':
    app.run(debug=True)