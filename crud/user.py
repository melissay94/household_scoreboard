from flask import jsonify, redirect
from models import db, User

# GET all users
def get_all_users():
  all_users = User.query.all()
  results = [user.as_dict() for user in all_users]
  return jsonify(results)

# GET a specific user
def get_user(id):
  user = User.query.get(id)
  if user:
    return jsonify(user.as_dict())
  else:
    raise Exception(f"Error getting user at {id}")

# POST a new user
def create_user(name, email):
  new_user = User(name=name, email=email)
  db.session.add(new_user)
  db.session.commit()
  return jsonify(new_user.as_dict())

# PUT a specific user
def update_user(id, name, email):
  user = User.query.get(id)
  print(name, code)
  if user:
    user.name = name or user.name
    user.code = email or user.email
    db.session.commit()
    return jsonify(user.as_dict())
  else:
    raise Exception(f"No User at {id}")

# DELETE a specific user
def destroy_user(id):
  user = User.query.get(id)

  if user:
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
  else:
    raise Exception(f"No User at {id}")
