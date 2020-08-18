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

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    print("Server received request for 'Home' page...")
    return "<h1>Welcome to the Climate App!</h1> </br>" + \
        f"Available Routes:<br/>" + \
        f"Precipitation Info: /api/v1.0/precipitation<br/>" + \
        f"Stations List: /api/v1.0/stations<br/>" + \
        f"Past 12 Months Data: /api/v1.0/tobs<br/>" + \
        f"Temp Stats (Start Date): /api/v1.0/<start><br/>" + \
        f"Temp Stats (Start to End Date):/api/v1.0/<start>/<end><br/>"
  
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation data
    results = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date<=date[0]).\
              group_by(Measurement.date).all()

    # Terminate Session
    session.close()

    # Create a dictionary 
    precip_dict = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations data
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Create a list
    station_list = list(np.ravel(results))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temp data
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
              filter(Measurement.date>=last_year, Measurement.station== active_stations[0][0]).order_by(Measurement.tobs).all()
  
    # Terminate session
    session.close()

    # Create a list
    temp_list = list(np.ravel(results))

    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query min, max, and average values since the given start date
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs).\
              filter(Measurement.date >= start).all()
                            
    # Terminate session
    session.close()
    
    # Create a list
    start_list = []
    for min_temp, avg_temp, max_temp in results:
        d = {}
        d["Min"] = min_temp
        d["Average"] = avg_temp
        d["Max"] = max_temp
        start_list.append(d)

    # Create a list
    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query min, max, and average values since the given start date
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs).\
              filter(Measurement.date >= start).\
              filter(Measurement.date <= end).all()
                            
    # Terminate session
    session.close()
    
    # Create a list
    start_end_list = []
    for min_temp, avg_temp, max_temp in results:
        d = {}
        d["Min"] = min_temp
        d["Average"] = avg_temp
        d["Max"] = max_temp
        start_end_list.append(d)

    # Create a list
    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)
