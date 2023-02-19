from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# Database Engine "be able to interact wit the DB"
engine = create_engine("postgres://xahhbjyonyshlt:10c1c96941ecfe60707533c0000b79b481c0bb185c585f4ae6cc5bdcc03b63a9@ec2-18-233-207-22.compute-1.amazonaws.com:5432/d3rloc3t9drveg") # DATABASE_URL = ENVIRONMENT *VARIABLE*
# run the database
db = scoped_session(sessionmaker(bind=engine))
while True:
	title = input("title: ")
	price = float(input("price: "))
	dsc = "معجنات مشكلة"
	category = input("category: ")

	db.execute("INSERT INTO products(title, price, dsc, category) VALUES(:title, :price, :dsc, :category)", 
		{"title": title, "price": price, "dsc": dsc, "category": category})
	db.commit()