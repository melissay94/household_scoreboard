from models import app, Household
from flask import jsonify, request
from crud.household import get_all_households, get_household, create_household, update_household, destroy_household
from crud.user import get_all_users, get_user, create_user, update_user, destroy_user

@app.errorhandler(Exception)
def unhandled_exception(e):
  app.logger.error(f"Unhandled Exception: {e}")
  message = e.__str__()
  return jsonify(message=message.split(":")[0])

@app.route("/households", methods=["GET", "POST"])
def household_all():
  if request.method == "GET":
    return get_all_households()
  
  return create_household(request.form["name"], request.form["code"])

@app.route("/households/<int:id>", methods=["GET", "PUT", "DELETE"])
def household_specific(id):
  if request.method == "GET":
    return get_household(id)
  elif request.method == "PUT":
    name = request.form["name"]
    code = request.form["code"]
    return update_household(id, name, code)
  else:
    return destroy_household(id)

@app.route("/users", methods=["GET", "POST"])
def user_all():
  if request.method == "GET":
    return get_all_users()
  
  return create_user(request.form["name"], request.form["email"])

@app.route("/users/<int:id>", methods=["GET", "PUT", "DELETE"])
def user_specific(id):
  if request.method == "GET":
    return get_user(id)
  elif request.method == "PUT":
    name = request.form["name"]
    email = request.form["email"]
    return update_user(id, name, email)
  else:
    return destroy_user(id)

