from flask import jsonify, redirect
from models import db, Chore

# GET all chores
def get_all_chores():
  all_chores = Chore.query.all()
  results = [chore.as_dict() for chore in all_chores]
  return jsonify(results)

# GET a specific chore
def get_chore(id):
  chore = Chore.query.get(id)
  if chore:
    return jsonify(chore.as_dict())
  else:
    raise Exception(f"Error getting chore at {id}")

# POST a new chore
def create_chore(name, description, difficulty):
  new_chore = Chore(name=name, description=description, difficulty=difficulty)
  db.session.add(new_chore)
  db.session.commit()
  return jsonify(new_chore.as_dict())

# PUT a specific chore
def update_chore(id, name, description, difficulty):
  chore = Chore.query.get(id)
  if chore:
    chore.name = name or chore.name
    chore.description = description or chore.description
    chore.difficulty = difficulty or chore.difficulty
    db.session.commit()
    return jsonify(chore.as_dict())
  else:
    raise Exception(f"No Chore at {id}")

# DELETE a specific chore
def destroy_chore(id):
  chore = Chore.query.get(id)

  if chore:
    db.session.delete(chore)
    db.session.commit()
    return redirect("/chores")
  else:
    raise Exception(f"No Chore at {id}")
