from uuid import uuid4
from flask import request, redirect, render_template, jsonify
from flask_login import login_user, login_required, current_user, logout_user
# from sqlalchemy.sql.functions import current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import json
from ext import db, app, lm
from models import Products, Users
from forms import RegisterForm, AuthForm, SellForm, RevForm

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "tiff"}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@lm.user_loader
def load_usr(uid):
    return Users.query.get(uid)


@app.route('/')
def index():
    carousel = Products.query.filter_by(tag="carousel").all()
    items = []
    if len(carousel) > 5:
        for i in range(1, 7):
            items.append((i, carousel[i - 1]))

    return render_template("index.html", items=items)


@app.route('/sign-up', methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        if len(Users.query.filter_by(email=form.email.data).all()) == 0:
            user = Users(name=form.name.data,
                         password=form.password.data,
                         id=str(uuid4().int),
                         email=form.email.data,
                         birthdate=form.date.data,
                         cart="[]",
                         rank=0)
            db.session.add(user)
            db.session.commit()
            return redirect("/sign-in")
        else:
            return redirect("/sign-up")
    else:
        print(form.errors)

    return render_template("signup.html", form=form)


@app.route('/sign-in', methods=["GET", "POST"])
def signin():
    form = AuthForm()

    if form.validate_on_submit():
        print("ji")
        if Users.query.filter_by(email=form.email.data).first():
            print("ka")
            user = Users.query.filter_by(email=form.email.data).first()

            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect("/")

        return redirect("/sign-in")
    else:
        print(form.errors)

    return render_template("signin.html", form=form)


@app.route('/sell', methods=["GET", "POST"])
@login_required
def sell():
    form = SellForm()

    if form.validate_on_submit():

        filename = secure_filename(form.f1.data.filename)
        form.f1.data.save('static/productIMGS/' + filename)
        print(filename)
        product = Products(
            name=form.name.data,
            price=form.price.data,
            image='static/productIMGS/' + filename,
            id=str(uuid4().int),
            description=form.description.data,
            tag="none",
            likes="[]",
            reviews="[]",
            author=current_user.get_id()
        )

        db.session.add(product)
        db.session.commit()
        return redirect("/")
    else:
        print(form.errors)

    return render_template("sell.html", form=form)


@app.route("/api/delete/<uid>")
def delete(uid):
    if Products.query.get(uid) != None and Products.query.get(uid).author == current_user.get_id() or Users.query.get(
            current_user.get_id()).rank == 1:
        db.session.delete(Products.query.get(uid))
        db.session.commit()

    return redirect("/")


@app.route("/api/search/")
def search():
    name = request.args.get("name")
    products = Products.query

    products = products.filter(Products.name.ilike(f"%{name}%"))

    products = products.all()
    page = 0
    data = [[]]
    i = 0
    for p in products:
        if i > 11:
            page += 1
            data.append([])
            i = 0

        txt = ""

        if current_user.get_id() in json.loads(p.likes):
            txt = "liked"

        data[page].append({
            "name": p.name,
            "price": p.price,
            "img": p.image,
            "desc": p.description,
            "id": p.id,
            "likes": json.loads(p.likes),
            "liked": txt,
            "author": p.author
        })
        i += 1

    return jsonify(data)


@app.route('/market')
def market():
    query = ""
    rank = 0
    if current_user.is_authenticated:
        usr = Users.query.get(current_user.get_id())
        rank = usr.rank

    if request.args.get("query") != None:
        query = request.args.get("query")
    return render_template("market.html", query=query, rank=rank)


@app.route("/toggle-like/<uid>", methods=["POST"])
@login_required
def tl(uid):
    product = Products.query.get(uid)
    liked = json.loads(product.likes)
    if current_user.get_id() in liked:
        liked.remove(current_user.id)
        product.likes = json.dumps(liked)
        db.session.commit()
        return jsonify([False])
    else:
        liked.append(current_user.get_id())
        product.likes = json.dumps(liked)
        db.session.commit()
        return jsonify([True])


@app.route("/listings/<uid>")
def listings(uid):
    p = Products.query.get(uid)

    txt = ""

    median = 0

    for r in json.loads(p.reviews):
        median += r["score"] / len(json.loads(p.reviews))

    if current_user.get_id() in json.loads(p.likes):
        txt = "liked"

    return render_template("listing.html", p=txt, product=p, reviews=json.loads(p.reviews), median=median)


@app.route("/review/<uid>", methods=["GET", "POST"])
@login_required
def review(uid):
    p = Products.query.get(uid)
    form = RevForm()

    if form.validate_on_submit():
        product = Products.query.get(uid)
        revs = json.loads(product.reviews)

        revs.append({
            "user_id": current_user.get_id(),
            "score": form.rate.data,
            "review": form.review.data,
            "name": load_usr(current_user.get_id()).name
        })

        product.reviews = json.dumps(revs)

        db.session.commit()

    return render_template("review.html", p=p, form=form)


@app.route('/edit/<pid>', methods=["GET", "POST"])
@login_required
def edit(pid):
    if Products.query.get(pid) != None and Products.query.get(pid).author == current_user.get_id() or Users.query.get(
            current_user.get_id()).rank == 1:
        edproduct = Products.query.get(pid)
        form = SellForm(
            name=edproduct.name,
            price=edproduct.price,
            description=edproduct.description
        )

        if form.validate_on_submit():

            filename = secure_filename(form.f1.data.filename)
            form.f1.data.save('static/productIMGS/' + filename)

            edproduct.name = form.name.data
            edproduct.description = form.description.data
            edproduct.price = form.price.data
            edproduct.image = 'static/productIMGS/' + filename

            db.session.commit()
            return redirect("/")
        else:
            print(form.errors)

        return render_template("sell.html", form=form)


@app.route('/api/add-to-cart/<pid>', methods=["GET"])
@login_required
def add_to_cart(pid):
    user = Users.query.get(current_user.get_id())
    if user != None and Products.query.get(pid) != None:
        cart = json.loads(user.cart)
        if pid in cart:
            return redirect("/listings/" + pid)
        else:
            cart.append(pid)
            user.cart = json.dumps(cart)
            db.session.commit()
            return redirect("/listings/" + pid)
    else:
        return jsonify([False])


@app.route("/cart")
@login_required
def cart():
    user = Users.query.get(current_user.get_id())
    ccart = json.loads(user.cart)
    products = []

    for pid in ccart:
        if Products.query.get(pid):
            products.append(Products.query.get(pid))

    return render_template("cart.html", cart=products)


@app.route("/api/remove/<uid>")
def rem(uid):
    user = Users.query.get(current_user.get_id())
    ccart = json.loads(user.cart)
    ccart.remove(uid)
    user.cart = json.dumps(ccart)
    db.session.commit()
    return redirect("/")


@app.route("/log-out")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/your-products")
def yp():
    return render_template("prods.html", cart=Products.query.filter_by(author=current_user.get_id()).all())