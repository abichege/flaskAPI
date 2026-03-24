# Rules of a REST API
# 1. Data is transferred as key value pairs called JSON
# Sending from JS as JSON objects -From python as dictionary
# 2.You must define routes/URL
# 3.You must define a http metthod. E.g-GET,POST,PUT,DELETE,PATCH
# 4.You must define a status code E.g-200,201,404,401,500
import sentry_sdk
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from database import Employee, Base, Authentication
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "abcdef123"

CORS(app,supports_credentials=True)

sentry_sdk.init(
    dsn="https://67d2ba4d320a12775969a976a2fa6a36@o4511095113908224.ingest.us.sentry.io/4511095125245952",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

jwt = JWTManager(app)

bcrypt = Bcrypt(app)

DATABASE_URL = "postgresql+psycopg2://postgres:blossomabigael@localhost:5432/vue_myduka"

# connecting SQLAlchemy to PSQL using engine function
engine = create_engine(DATABASE_URL, echo=False)

# create session to call query methods
session = sessionmaker(bind=engine)
my_session = session()

# create tables automatically
Base.metadata.create_all(engine)

allowed_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]


@app.route('/', methods=allowed_methods)
def home():
    food
    method = request.method.lower()
    if method == "get":
        return jsonify({"Flask APi Version": "1.0"}), 200
    else:
        return jsonify({"msg": "Method not allowed"}), 405


@app.route("/employees", methods=allowed_methods)
# @jwt_required()
def employees():
    try:
        method = request.method.lower()
        if method == "get":
            employee_list = []
            query = select(Employee)
            my_employees = list(my_session.scalars(query).all())

            for employee in my_employees:
                employee_list.append({"id": employee.id,
                                      "name": employee.name,
                                      "location": employee.location,
                                      "age": employee.age})

            return jsonify({"data": employee_list}), 200
        elif method == "post":
            # convert json to dictionary
            data = request.get_json()
            # check if all fields are received
            if data["name"] == "" or data["location"] == "" or data["age"] == "":
                return jsonify({"msg": "All fields required"}), 401
            else:
                # employee_list.append(data)/store employee in employees tables using SQLAlchemypip
                new_employee = Employee(
                    name=data["name"], location=data["location"], age=data["age"])
                my_session.add(new_employee)
                my_session.commit()
                my_session.close()

                return jsonify({"msg": "Successfully added employee"}), 201
        else:
            return jsonify({"msg": "Method not allowed"}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/register', methods=allowed_methods)
def register():
    try:
        method = request.method.lower()

        if method == "post":
            data = request.get_json()

            # check if all fields are provided
            if data["full_name"] == "" or data["email"] == "" or data["password"] == "":
                return jsonify({"msg": "Full name, email and password cannot be empty"}), 400

            # check if user already exists
            existing_user = my_session.query(
                Authentication).filter_by(email=data["email"]).first()
            if existing_user:
                return jsonify({"msg": "Email already registered"}), 409

            # hash password
            hashed_password = bcrypt.generate_password_hash(
                data["password"]).decode("utf-8")

            # create new user
            new_auth = Authentication(
                email=data["email"],
                hashed_password=hashed_password,
                full_name=data["full_name"],
                created_at=datetime.utcnow()
            )

            my_session.add(new_auth)
            my_session.commit()

            # generate token
            token = create_access_token(identity=data["email"])

            return jsonify({
                "msg": "User created",
                "token": token
            }), 201

        else:
            return jsonify({"msg": "Method not allowed"}), 405

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/login', methods=allowed_methods)
def login():
    try:
        method = request.method.lower()

        if method == "post":
            data = request.get_json()

            email = data.get("email")
            password = data.get("password")

            # validate input
            if not email or not password:
                return jsonify({"msg": "Email and password required"}), 400

            # check if user exists
            query = select(Authentication).where(Authentication.email == email)
            auth = my_session.scalars(query).first()

            if not auth:
                return jsonify({"msg": "Invalid email"}), 401

            # verify password
            if not bcrypt.check_password_hash(auth.hashed_password, password):
                return jsonify({"msg": "Invalid password"}), 401

            # generate token
            token = create_access_token(identity=email)

            return jsonify({
                "msg": "Login successful",
                "user": {
                    "id": auth.id,
                    "full_name": auth.full_name,
                    "email": auth.email
                },
                "token": token
            }), 200

        else:
            return jsonify({"msg": "Method not allowed"}), 405

    except Exception as e:
        return jsonify({"error": str(e)}), 500


app.run(debug=True)
