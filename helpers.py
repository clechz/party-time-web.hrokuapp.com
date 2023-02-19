import os
import smtplib
from email.message import EmailMessage
from functools import wraps
from random import randint
from flask import redirect, render_template, request, session


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def usd(n):
    n = float(n)
    n /= 3.75
    return  f"{n:.2f}"

def generate_verf():
    return str(randint(1000, 9999))

def send_email(subject, body, to):

    msg = EmailMessage()
    msg["Subject"] = str(subject)
    msg["From"] = "help.ptime@gmail.com"
    msg["To"] = str(to)

    msg.set_content(str(body))
    print(body)
    # NEW UPDATE FOR COLLGES: Function doesn't work 
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("help.ptime@gmail.com", "tsbydvfmibwqeelv")
        smtp.send_message(msg)

def send_sms_verf(number):
    import requests
    resp = requests.post('https://textbelt.com/text', {
      'phone': "+966"+str(number),
      'message': f'Hello Baba your verification number id {verf()}',
      'key': 'textbelt',
    })
    print(resp.json())

def is_valid_email(email):
    if email:
        if '@' in email and '.' in email and email[-1] != '@' and email[-1] != '.' and email[0] != '@':
            at_count = 0
            dot_count = 0

            for char in email:

                if at_count > 1:
                    print(False)
                    return False

                if char == '@':
                    if email[email.index(char)+1] == '.':
                        print(False)
                        return False

                    at_count+=1

                elif char == '.':
                    dot_count+=1

            print(True)
            return True

        else:
            print(False)
            return False

    else:
        print(False)
        return False

def is_valid_password(password):
    if len(password) >= 6:
        return True
    else:
        return False

def is_valid_phone(phone):
    digits = 0
    print(phone)

    for char in phone:
        if char.isdigit():
            digits+=1

    print(digits)
    print(len(phone))
    print(phone[0:2])
    if len(phone) == digits == 10 and phone[0:2] == "05":
        print(True)
        return True
    
    else:
        print(False)
        return False
	
def init():
    cart = request.form.get("cart")
    if cart:
        cart = cart.split()

        if session.get("cart"):
            for i in range(len(cart)):
                session["cart"].append(cart[i])
        else:
            session["cart"] = cart
        
        print("done init")
    

def clear_cookies():
    print(request.cookies.get("cart"))
    session.clear()


def sub_products(cart, stock):
    print()
    stock = stock.split()
    new_stock = stock
    for p in list(dict.fromkeys(stock)):
        # if user ordered this p
        if p in cart:
            # for each one of p remove from stock
            for i in range(cart.count(p)):
                new_stock.remove(p)
                print("removed")

    print()
    print(new_stock)
    str_new_stock = ""
    for p in new_stock:
        str_new_stock+= ' ' + p
        
    return str_new_stock

