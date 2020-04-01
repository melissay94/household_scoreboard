from flask import jsonify, redirect
from models import db, Household

# GET all households
def get_all_households():
  all_households = Household.query.all()
  results = [household.as_dict() for household in all_households]
  return jsonify(results)

# GET a specific household
def get_household(id):
  household = Household.query.get(id)
  if household:
    return jsonify(household.as_dict())
  else:
    raise Exception(f"Error getting user at {id}")

# POST a new household
def create_household(name, code):
  new_household = Household(name=name, code=code)
  db.session.add(new_household)
  db.session.commit()
  return jsonify(new_household.as_dict())

# PUT a specific household
def update_household(id, name, code):
  household = Household.query.get(id)
  print(name, code)
  if household:
    household.name = name or household.name
    household.code = code or household.code
    db.session.commit()
    return jsonify(household.as_dict())
  else:
    raise Exception(f"No Household at {id}")

# DELETE a specific household
def destroy_household(id):
  household = Household.query.get(id)

  if household:
    db.session.delete(household)
    db.session.commit()
    return redirect("/households")
  else:
    raise Exception(f"No Household at {id}")
