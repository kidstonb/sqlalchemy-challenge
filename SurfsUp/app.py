import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite", pool_pre_ping=True)
Base = automap_base()
Base.prepare(autoload_with=engine)
Measurement = Base.classes.measurement

# Saving station list manually 
stations = [(1, 'USC00519397', 'WAIKIKI 717.2, HI US'),
 (2, 'USC00513117', 'KANEOHE 838.1, HI US'),
 (3, 'USC00514830', 'KUALOA RANCH HEADQUARTERS 886.9, HI US'),
 (4, 'USC00517948', 'PEARL CITY, HI US'),
 (5, 'USC00518838', 'UPPER WAHIAWA 874.3, HI US'),
 (6, 'USC00519523', 'WAIMANALO EXPERIMENTAL FARM, HI US'),
 (7, 'USC00519281', 'WAIHEE 837.5, HI US'),
 (8, 'USC00511918', 'HONOLULU OBSERVATORY 702.2, HI US'),
 (9, 'USC00516128', 'MANOA LYON ARBO 785.2, HI US')]

# Flask Setup
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Weather Oberservation API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/precipitation")
def precip():
    session = Session(engine)

    prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(func.strftime(Measurement.date) > '2016-08-23').\
    group_by(Measurement.date).\
    all()

    session.close()

    return jsonify(prcp)

@app.route("/stations")
def station():
    return jsonify(stations)

@app.route("/tobs")
def t_obs():
    session = Session(engine)

    temp = session.query(Measurement.tobs)\
    .filter(Measurement.station == 'USC00519281')\
    .filter(func.date(Measurement.date) > '2016-08-23')\
    .all()

    session.close()

    return jsonify(temp)

# @app.route("/<start>")

# @app.route("/<start>/<end>")

if __name__ == "__main__":
    app.run(debug=True)