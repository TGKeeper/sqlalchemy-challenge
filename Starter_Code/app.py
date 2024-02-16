# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func

import pandas as pandas
import numpy as np
import datetime as dt

# APP
app = Flask(__name__)

#################################################
# Database Setup
#################################################

# same engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
# Stores the base(s) as an object reference
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Routes
#################################################

#home route/landing page of app
@app.route("/")

def home():
    return(f"<center><h1> Mel's Local API for Hawaii Climate Analysis </center></h1>"

    f"<center><h3>api/v1.0/precipitation</center></h>"
    f"<center><h3>api/v1.0/stations</center></h>"
    f"<center><h3>api/v1.0/tobs</center></h>"

    )


# precip route
@app.route("/api/v1.0/precipitation")

def precip():
    last12 = dt.date(2017, 8, 23) - dt.timedelta(days=365)
 
    last12_q = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last12).all()

    session.close()

    # make dictionary
    precip_dict = {date: prcp for date, prcp in last12_q}

	# make json
    return jsonify(precip_dict)


# station route
@app.route("/api/v1.0/stations")

def stations():

    stations_q = session.query(Station.station).all()

    session.close()

    # make LIST
    staion_List = list(np.ravel(stations_q)) 

	# make json
    return jsonify(staion_List)


# observed temp route
@app.route("/api/v1.0/tobs")

def obs_temps():

    last12 = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    tobs = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").\
    filter(Measurement.date >= last12).all()

    session.close()

    # make LIST
    tobs_List = list(np.ravel(tobs)) 

	# make json
    return jsonify(tobs_List)



# start & end routes? 
@app.route("/api/v1.0/<start>")

@app.route("/api/v1.0/<start>/<end>")

def dateStats(start=None, end=None):
    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

    if not end: 

        startDate = dt.datetime.strptime(start, "%m%d%Y")

        results = session.query(*selection).filter(Measurement.date >= startDate).all()

        session.close()

        results_List = list(np.ravel(results))

        return jsonify(results_List)
    
    else:

        startDate = dt.datetime.strptime(start, "%m%d%Y")
        endDate = dt.datetime.strptime(end, "%m%d%Y")


        results = session.query(*selection)\
            .filter(Measurement.date >= startDate)\
            .filter(Measurement.date <= endDate).all()

        session.close()

        results_List = list(np.ravel(results))

        return jsonify(results_List)


if __name__ == '__main__':
    app.run(debug=True)
