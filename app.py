from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)


@app.route("/")
def root():
    """Render homepage."""

    return render_template("index.html")

@app.route("/api/cupcakes")
def get_all_cupcakes():
    cupcakes = Cupcake.query.all()
    serialized_cupcakes = [{"id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image} for cupcake in cupcakes]
    return jsonify(cupcakes=serialized_cupcakes)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized_cupcake = {"id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image}
    return jsonify(cupcake=serialized_cupcake)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    data = request.get_json()
    new_cupcake = Cupcake(flavor=data["flavor"], size=data["size"], rating=data["rating"], image=data.get("image"))
    db.session.add(new_cupcake)
    db.session.commit()
    serialized_cupcake = {"id": new_cupcake.id, "flavor": new_cupcake.flavor, "size": new_cupcake.size, "rating": new_cupcake.rating, "image": new_cupcake.image}
    return (jsonify(cupcake=serialized_cupcake), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake with the id passed in the URL."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.get_json()
    cupcake.flavor = data["flavor"]
    cupcake.size = data["size"]
    cupcake.rating = data["rating"]
    cupcake.image = data["image"]
    db.session.commit()
    updated_cupcake = {"id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image}
    return jsonify(cupcake=updated_cupcake)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake with the id passed in the URL."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")


if __name__ == '__main__':
    app.run(debug=True)
