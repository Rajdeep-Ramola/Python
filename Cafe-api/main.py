from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "img_url": self.img_url,
            "map_url": self.map_url,
            "amenities": {
                "can_take_calls": self.can_take_calls,
                "coffee_price": self.coffee_price,
                "has_sockets": self.has_sockets,
                "has_toilet": self.has_toilet,
                "has_wifi": self.has_wifi,
                "seats": self.seats
            }
        }

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record
#to get information about all cafes
@app.route("/all")
def get_all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

#to get information about a random cafe
@app.route("/random")
def get_randomcafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe={
        # "id": random_cafe.id, if we don't want a particular field in response we can simply omit it
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,

        # Put some properties in a sub-category
        "amenities": {
            "seats": random_cafe.seats,
            "has_toilet": random_cafe.has_toilet,
            "has_wifi": random_cafe.has_wifi,
            "has_sockets": random_cafe.has_sockets,
            "can_take_calls": random_cafe.can_take_calls,
            "coffee_price": random_cafe.coffee_price,
        }
    })

#to get cafes in a particular location
@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404

# HTTP POST - Create Record
#to add a new cafe
@app.route("/add", methods=["POST"])
def post_new_cafe():
    name = request.form.get("name")
    location = request.form.get("loc")
    coffee_price = request.form.get("coffee_price")

    if not name or not location or not coffee_price:
        return jsonify(error="Missing required fields"), 400

    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

# HTTP PUT/PATCH - Update Record
#to update coffee price
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price=new_price
        db.session.commit()
        return jsonify(response={'Success':'Successfully updated the coffee price'}),200
    else:
        return jsonify(error={'Error':'Cafe not found'}),404

# HTTP DELETE - Delete Record
#to delete a cafe with particular id
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        try:
            cafe = db.session.get(Cafe, cafe_id)
        except AttributeError:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
        else:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

if __name__ == '__main__':
    app.run(debug=False)

#Documentation for API- https://documenter.getpostman.com/view/46903694/2sB3Hopz7Z
