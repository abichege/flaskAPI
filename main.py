# Rules of a REST API
# 1. Data is transferred as key value pairs called JSON
# Sending from JS as JSON objects -From python as dictionary
# 2.You must define routes/URL
# 3.You must define a http metthod. E.g-GET,POST,PUT,DELETE,PATCH
# 4.You must define a status code E.g-200,201,404,401,500
from flask import Flask, jsonify, request
from sqlalchemy import create_engine,select
from sqlalchemy.orm import sessionmaker
from database import User,Base
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
# , origins=["http://127.0.0.1:5500"]

DATABASE_URL = "postgresql+psycopg2://postgres:blossomabigael@localhost:5432/vue_myduka"

# connecting SQLAlchemy to PSQL using engine function
engine = create_engine(DATABASE_URL, echo=False)

# create session to call query methods
session = sessionmaker(bind=engine)
my_session=session()

# create tables automatically
Base.metadata.create_all(engine)

allowed_methods = ["GET", "POST", "PUT", "DELETE","PATCH"]
user_list = []


@app.route('/', methods=allowed_methods)
def home():
    method = request.method.lower()
    if method == "get":
        return jsonify({"Flask APi Version": "1.0"}), 200
    else:
        return jsonify({"msg": "Method not allowed"}), 405


@app.route("/users", methods=allowed_methods)
def users():
    try:
        method = request.method.lower()
        if method == "get":
            user_list = []
            query=select(User)
            my_users=list(my_session.scalars(query).all())
            # print(users)

            for user in my_users:
                user_list.append({"id":user.id,
                                "name":user.name,
                                "location":user.location})

            return jsonify({"data": user_list}), 200
        elif method == "post":
            # convert json to dictionary
            data = request.get_json()
            # check if all fields are received
            if data["name"] == "" or data["location"] == "":
                return jsonify({"msg": "All fields required"}), 401
            else:
                # user_list.append(data)/store user in users tables using SQLAlchemypip
                new_user = User(name=data["name"], location=data["location"])
                my_session.add(new_user)
                my_session.commit()
                my_session.close()

                return jsonify({"msg": "Successfully added user"}), 201
        else:
            return jsonify({"msg": "Method not allowed"}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
    
@app.route('/register',methods=allowed_methods)   
def register():
    # convert json to dictionary
            data = request.get_json()
            # check if all fields are received
            if data["username"] == "" or data["email"] == "" or data["password"] == "":
                return jsonify({"msg": "All fields required"}), 401
            else:
                # user_list.append(data)/store user in users tables using SQLAlchemypip
                new_user = User(username=data["username"], email=data["email"],password=data["password"])
                my_session.add(new_user)
                my_session.commit()
                my_session.refresh(new_user)

                return jsonify({"msg": "Successfully added user"}), 201



app.run(debug=True)
