from datetime import datetime as dt
from pytz import timezone, UTC
import os
import smtplib
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, redirect, flash, session, request, url_for, abort, make_response
from helpers import login_required, usd, generate_verf, send_email, is_valid_password, is_valid_email, is_valid_phone, clear_cookies, sub_products
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sitemap import Sitemap

'''GLOBAL'''

CATEGORIES = ["grape", "pastry", "cake"]


# app var
app = Flask(__name__)
app.secret_key = "postgres://wyqaudmtkaunkt:ba83af477a1b75b1f32acf2b7ab624616e0fd983cc3cd184f447bb21bbcba5de@ec2-54-173-77-184.compute-1.amazonaws.com:5432/d8enpsvsceiefc,abdullah.abdulrhman.alzhrani@gmail.com,saeed.abdullah11"
ext = Sitemap(app=app)

# Database Engine "To be able to interact wit the DB"
engine = create_engine("postgres://wyqaudmtkaunkt:ba83af477a1b75b1f32acf2b7ab624616e0fd983cc3cd184f447bb21bbcba5de@ec2-54-173-77-184.compute-1.amazonaws.com:5432/d8enpsvsceiefc") # DATABASE_URL = ENVIRONMENT *VARIABLE*
# run the database
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    '''rendering index page'''

    return render_template("index.html", dt=dt.now())



# @app.route("/sitemap.xml")
# def sitemap():

#     SM = render_template("sitemap.xml")
#     response = make_response(SM)
#     response.headers["Content-Type"] = "application/xml"

#     return response


@app.route("/menu", methods=["GET", "POST"])
def menu():

    stock = db.execute("SELECT * FROM stock").fetchone()
    # later is bigger
    if stock["date"] > dt.now():

        if request.method == "POST":
            order_type = request.form.get("order_type")
            order_date = request.form.get("order-date")

            if order_type == "now":
                session["order_type"] = order_type

            elif order_type == "pre":
                
                session["order_type"] = order_type
                session["order_date"] = order_date

            print(session["order_type"])
            return redirect("/menu")

        else:        

            if session.get("order_type"):
                return render_template("menu.html", categories=CATEGORIES)

            else:
                return render_template("get_order_type.html")

    else:

        return f"<script>alert('التوصيل متوفر من 3 العصر الى {stock['date'].hour-12+3}');\n window.location.href='/'</script>"


@app.route("/menu/<string:category>")
def menu_products(category):

    stock = db.execute("SELECT * FROM stock").fetchone()
    # after is bigger
    if stock["date"] > dt.now():
        print("cart did'not expire")

        if session.get("order_type"):
            rows = db.execute("SELECT * FROM products WHERE category = :category", {"category": category}).fetchall()
            products = []

            for row in rows:
                products.append({
                    "id": str(row["id"]),
                    "title": row["title"],
                    "price": row["price"],
                    "dsc": row["dsc"]
                })

            cart_count = len(request.cookies.get("cart")) if request.cookies.get("cart") else 0
            cart = request.cookies.get("cart")
            
            date = stock['date']
            print(stock['date'].month-1)
            date.replace(month=date.month-1)
            return render_template("menu_products.html",
             products=products, cart_count=cart_count, cart=cart, stock=stock["products"], date=date)

        else:
            return redirect("/menu")

    else:
        return f"<script>alert('التوصيل متوفر من 3 العصر الى {stock['date'].hour-12+3}');\n window.location.href='/'</script>"


@app.route("/info", methods=["GET", "POST"])
def info():

    stock = db.execute("SELECT * FROM stock").fetchone()
    # later is bigger
    if stock["date"] > dt.now():

        cart = request.cookies.get("cart")
        if request.method == "POST" and cart:

            phone = str(request.form.get("phone"))
            name = request.form.get("name")
            dt.now

            if len(phone) == 9:

                phone = f"0{phone}"

            if is_valid_phone(phone) and name:
                print("valid order credintials")
                session["order"] = {"phone": phone, "name": name}
                stock = db.execute("SELECT * FROM stock").fetchone()
                time = str(dt.now())
                # send a message to client
                # add credintials to DB1        Q

                # send a message to saeed DONE
                # insert order to DB DONE
                # delete products from stock DONE
                # clear cart DONE

                db.execute("INSERT INTO orders (name, phone, products, time) VALUES (:name, :phone, :products, :time)",
                    {"name": name, "phone": phone, "products": cart, "time":time})

                order = db.execute("SELECT id, name, phone, products FROM orders WHERE phone=:phone AND time=:time AND name=:name AND products=:products",
                    {"name": name, "phone": phone, "products": cart, "time":time}).fetchone()
                
                if session.get("order_type") == "pre":
                    print(f"type is pre: {session['order_date']}")
                    send_email(order["id"], f"\n طلب مسبق {session['order_date']} {order}", "help.ptime@gmail.com")

                else:
                    # update stock
                    new_stock = sub_products(cart, stock["products"])
                    db.execute("UPDATE stock SET products=:new_stock", {"new_stock": new_stock})                    
                    print(f"type is now")
                    send_email(order["id"], f"{order}", "help.ptime@gmail.com")

                db.commit()

                # for the next order
                session["order_type"] = ""
                
                if session.get("order_date"):
                    session["order_date"] = ""

                return render_template("success.html")
            
            else:
                flash("حدث خطأ ما")
                return redirect("/login")

        else:
            if cart:
                return render_template("info.html")

            else:
                return redirect("/menu")

    else:
        return f"<script>alert('التوصيل متوفر من 3 العصر الى {stock['date'].hour-12+3}');\n window.location.href='/'</script>"


@app.route("/cart")
def cart():

    stock = db.execute("SELECT * FROM stock").fetchone()
    # later is bigger
    if stock["date"] > dt.now():

        if request.cookies.get("cart"):
            cart = []
            subtotal = 0
            shipping = 15

            for product in request.cookies.get("cart").split():
                row = db.execute("SELECT * FROM products WHERE id = :id", {"id": product}).fetchone()
                subtotal+=row["price"]
                cart.append(row) 


            total = subtotal + shipping
            print(cart)

            return render_template("cart.html",
            cart=cart, total=total, subtotal=subtotal, p_sum=request.cookies.get("len_cart"), shipping=shipping)
        
        else:
            return render_template("cart.html")

    else:
        return f"<script>alert('التوصيل متوفر من 3 العصر الى {stock['date'].hour-12+3}');\n window.location.href='/'</script>"


# @app.route("/products/<string:id>")
# def product(id):

#     product = db.execute("SELECT * FROM products WHERE id = :id", {"id": id}).fetchone()
#     db.commit()

#     if product:
#         return render_template("product.html", id=id, product=product, price=usd(product["price"]))
#     else:
#         return redirect("/")


@app.route("/find")
def find():

    return render_template("find.html")


@login_required
@app.route("/profile")
def profile():

    return render_template("profile.html", email=session.get("email"))


# @login_required
# @app.route("/profile/email", methods=["POST", "GET"])
# def profile_email():


@login_required
@app.route("/profile/password")
def profile_password():

    return render_template("redirect.html", to=url_for("forgot_password"), email=session.get("email"))


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        
        clear_cookies()
        # form input / user credintials
        email = request.form.get("email")
        password = request.form.get("password")
        # user info
        user = db.execute("SELECT * FROM users WHERE email = :email LIMIT 1", {"email": email}).fetchall()

        # if user credintials is true
        if len(user) == 1 and check_password_hash(user[0]["hash"], password):

            session["user_id"] = user[0]["id"]
            session["email"] = user[0]["email"]

            return redirect("/")
        
        else:

            flash("البريد الإلكتروني أوكلمةالمرور خطأ", "error")
            return redirect("/login")

    else:

        return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        
        # form input / user credintials
        email = request.form.get("email")
        password = request.form.get("password")
        verify = request.form.get("verify")       

        # user info
        user = db.execute("SELECT * FROM users WHERE email = :email LIMIT 1", {"email": email}).fetchall()

        # if user dosen't exist
        if len(user) == 0:
            if verify:
                print(session["signup_verify"])
                if verify == session["signup_verify"]:  # && datetime < expiry datetime:
                    # hash password
                    hash = generate_password_hash(session["signup"]["password"])
                    email = session["signup"]["email"]
                    # insert new user to the database
                    db.execute("INSERT INTO users (email, hash) VALUES (:email, :hash)", {"email": email, "hash": hash})
                    db.commit()
                    # select new user from the database 
                    user = db.execute("SELECT * FROM users WHERE email = :email LIMIT 1", {"email": email}).fetchall()

                    session["user_id"] = user[0]["id"]
                    session["email"] = user[0]["email"]

                    return redirect("/")

                else: 
                    if session.get("verify"):
                        clear_cookies()

                    flash("رمز التفعيل خطأ يرجى التأكد من البريد الإلكتروني و المحاولة لاحقا")
                    return redirect("/signup")


                if session.get("verify"):
                    clear_cookies()

                    flash("رمز التفعيل خطأ يرجى التأكد من البريد الإلكتروني و المحاولة لاحقا")
                    return redirect("/signup")

            elif is_valid_email(email) and is_valid_password(password):

                verf = generate_verf()
                session["signup_verify"] = verf
                session["verify_expiry"] = "none"
                session["signup"] = {}
                session["signup"]["password"] = password
                session["signup"]["email"] = email

                subject = "رمز تحقق partytime | موعد الفل"
                body = f"رمز التفعيل الخاص بك هو{verf}, تنتهي صلاحية رمز التفعيل بعد دقيقه من الآن\nاذا كنت تجهل مصدر هذه الرساله يمكنك تجاهلها"
                to = email
                
                send_email(subject, body, to)
                print(verf)
                return render_template("verify.html", email=email)

            else:
                flash("البريد الإلكتروني الذي ادخلتة غير صالح الرجاء التأكد من البريد و المحاولة لاحقا")
                clear_cookies()   
                return redirect("/signup")

        else:

            flash("البريد الإلكتروني الذي ادخلتة غير صالح الرجاء التأكد من البريد و المحاولة لاحقا")
            return redirect("/login")
    else:

        return render_template("signup.html")


@app.route("/logout")
def logout():

    clear_cookies()
    return redirect("/")


@app.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():

    if request.method == "POST":
        email = request.form.get("email")
        verify = request.form.get("verify")
        token = request.form.get("token")
        print(email)
        if verify:

            # TODO maybe change validation to Javascript
            if verify == session["forgot_password_verify"] != None:  # && datetime < expiry datetime:
                
                token = generate_verf()
                session["token"] = token
                return render_template("change_password.html", email=session.get("email"), token=token)
            
            else:
                if session.get("forgot_password_verify"):
                    clear_cookies()

                flash("رمز التفعيل خطأ يرجى التأكد من البريد الإلكتروني و المحاولة لاحقا")
                return redirect("/login")


        if is_valid_email(email):
            user = db.execute("SELECT email FROM users WHERE email = :email", {"email": email}).fetchall()

            if len(user) == 1:

                verf = generate_verf()
                session["forgot_password_verify"] = verf
                session["email"] = email

                subject = "partytime | رمز تحقق"
                body = f"رمز التفعيل الخاص بك هو{verf}, تنتهي صلاحية رمز التفعيل بعد دقيقه من الآن\nاذا كنت تجهل مصدر هذه الرساله يمكنك تجاهلها"
                to = email
                
                send_email(subject, body, to)
                return render_template("verify.html", email=email)

            else: 

                flash("البريد الإلكتروني الذي ادخلتة غير صالح الرجاء التأكد من البريد و المحاولة لاحقا")
                return redirect("/login")


        if str(token) == str(session.get("token")) and token and is_valid_password(request.form.get("password")):
            clear_cookies()
            password = request.form.get("password")
            hash = generate_password_hash(password)
            user = db.execute("UPDATE users SET hash = :hash", {"hash": hash})
            db.commit()
            flash("تم تغيير كلمة المرور بنجاح")
            return redirect("/login")

        else:
            clear_cookies() 
            flash("حدث خطأ ما")
            return redirect("/login")

    else:
        # TODO 
        clear_cookies()   
        return render_template("get_email.html")


@app.errorhandler(404)
def not_found(e):
    
    return render_template("errs/404.html")


@app.errorhandler(500)
def not_found(e):

    return render_template("errs/505.html")


# @app.route("/dashboard/saeed/add-stock", methods=["GET", "POST"])
# def dashboard():


if __name__ == "__main__":
    app.run(debug=True)


# 3175 Lines Of Code.
# end of (Party Time).
# Built By Abdullah A. Alzhrani | @ia.zh.