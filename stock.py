from datetime import datetime as dt, date as d, time as t
from pytz import timezone, UTC
from app import db
''' erlier is smaller '''
products = input("products: ")

hour = 10 + 12 
tomowrow = d.today().replace(day=d.today().day+1)
today = d.today() 
		  # if the current time is after the closing time
day = today if t().hour > hour else tomowrow

date = dt(day.year, day.month, day.day, hour, 0, 0, 0)

db.execute("UPDATE stock SET products=:products, date=:date", {"date": date, "products": products})
db.commit()
print("closing time is:", date)