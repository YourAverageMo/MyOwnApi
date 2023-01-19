import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dict = {
            column: str(getattr(self, column))
            for column in self.__table__.c.keys()
        }
        return dict


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def random_cafe():

    def get_random_cafe():
        # Apparently this is the quickest way to get a random row from a database that may become large / Scalability
        # Firstly, get the total number of rows in the database
        row_count = Cafe.query.count()
        # Generate a random number for skipping some records
        random_offset = random.randint(0, row_count - 1)
        # Return the first record after skipping random_offset rows
        random_cafe = Cafe.query.offset(random_offset).first()
        return random_cafe

    random_cafe = get_random_cafe()
    return jsonify(random_cafe.to_dict())


@app.route("/all")
def all():
    all_cafes = Cafe.query.all()
    all_cafes = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(all_cafes)


@app.route("/search")
def search():
    requested_cafe = request.args.get("loc")
    all_cafes = Cafe.query.all()
    search_results = []
    for cafe in all_cafes:
        if cafe.location == requested_cafe.title():
            search_results.append(cafe.to_dict())
    if search_results == []:
        return {
            "error": {
                "Not Found": "Sorry, We dont have a cafe at that location"
            }
        }
    else:
        return search_results


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record

if __name__ == '__main__':
    app.run(debug=True)
