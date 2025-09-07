from flask import Flask, render_template, request, redirect, url_for
from models import db, Sneaker, Brand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sneakerstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# --- ROUTES SNEAKER ---
@app.route("/")
def home():
    sneakers = Sneaker.query.all()
    return render_template("home.html", sneakers=sneakers)

@app.route("/sneakers/add", methods=["GET", "POST"])
def add_sneaker():
    brands = Brand.query.all()
    if request.method == "POST":
        name = request.form["name"]
        size = request.form["size"]
        color = request.form["color"]
        type_ = request.form["type"]
        brand_id = request.form["brand_id"]
        sneaker = Sneaker(name=name, size=size, color=color, type=type_, brand_id=brand_id)
        db.session.add(sneaker)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("sneakers_add.html", brands=brands)

@app.route("/sneakers/edit/<int:id>", methods=["GET", "POST"])
def edit_sneaker(id):
    sneaker = Sneaker.query.get_or_404(id)
    brands = Brand.query.all()
    if request.method == "POST":
        sneaker.name = request.form["name"]
        sneaker.size = request.form["size"]
        sneaker.color = request.form["color"]
        sneaker.type = request.form["type"]
        sneaker.brand_id = request.form["brand_id"]
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("sneakers_edit.html", sneaker=sneaker, brands=brands)

@app.route("/sneakers/delete/<int:id>")
def delete_sneaker(id):
    sneaker = Sneaker.query.get_or_404(id)
    db.session.delete(sneaker)
    db.session.commit()
    return redirect(url_for('home'))

# --- ROUTES BRANDS ---
@app.route("/brands")
def brands_home():
    brands = Brand.query.all()
    return render_template("brands_home.html", brands=brands)

@app.route("/brands/add", methods=["GET", "POST"])
def add_brand():
    if request.method == "POST":
        name = request.form["name"]
        brand = Brand(name=name)
        db.session.add(brand)
        db.session.commit()
        return redirect(url_for('brands_home'))
    return render_template("brands_add.html")

@app.route("/brands/edit/<int:id>", methods=["GET", "POST"])
def edit_brand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        brand.name = request.form["name"]
        db.session.commit()
        return redirect(url_for('brands_home'))
    return render_template("brands_edit.html", brand=brand)

@app.route("/brands/delete/<int:id>")
def delete_brand(id):
    brand = Brand.query.get_or_404(id)
    db.session.delete(brand)
    db.session.commit()
    return redirect(url_for('brands_home'))

if __name__ == "__main__":
    app.run(debug=True)
