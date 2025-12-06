from market import app, bcrypt
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user
from market.db_connect import get_connection


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    if request.method == "POST":

        # ----- PURCHASE -----
        purchased_item = request.form.get("purchased_item")
        p_item = Item.get_by_name(purchased_item)

        if p_item:
            if current_user.budget >= p_item.price:
                p_item.buy(current_user)
                flash(f"You purchased {p_item.name}!", category="success")
            else:
                flash("Not enough money!", category="danger")

        # ----- SELL -----
        sold_item = request.form.get("sold_item")
        s_item = Item.get_by_name(sold_item)

        if s_item:
            owned = [i.name for i in Item.get_owned_items(current_user.id)]
            if s_item.name in owned:
                s_item.sell(current_user)
                flash(f"You sold {s_item.name}!", category="success")
            else:
                flash("You do not own this item!", category="danger")

        return redirect(url_for("market_page"))

    items = Item.get_available_items()
    owned_items = Item.get_owned_items(current_user.id)

    return render_template(
        "market.html",
        items=items,
        owned_items=owned_items,
        purchase_form=purchase_form,
        selling_form=selling_form
    )


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password1.data).decode("utf-8")

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (username, email_address, password_hash, budget)
                VALUES (%s, %s, %s, %s)
            """, (form.username.data, form.email_address.data, hashed_pw, 1000))
        conn.commit()

        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s", (form.username.data,))
            user = cursor.fetchone()
        conn.close()

        login_user(User(**user))
        flash("Account created!", category="success")
        return redirect(url_for("market_page"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
        conn.close()

        if user:
            user_obj = User(**user)
            if user_obj.check_password_correction(password):
                login_user(user_obj)
                flash(f"Logged in as {user_obj.username}", category="success")
                return redirect(url_for("market_page"))

        flash("Wrong username or password", category="danger")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("Logged out!", category="info")
    return redirect(url_for("home_page"))






