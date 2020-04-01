from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost/household_scoreboard"

db = SQLAlchemy(app)

household_chores = db.Table("household_chores",
  db.Column("household_id", db.Integer, db.ForiegnKey("households.id"), primary_key=True),
  db.Column("chore_id", db.Integer, db.ForiegnKey("chores.id"), primary_key=True)
)

user_chores = db.Table("user_chores",
  db.Column("user_id", db.Integer, db.ForiegnKey("users.id"), primary_key=True),
  db.Column("chore_id", db.Integer, db.ForiegnKey("chores.id"), primary_key=True)
)

class Household(db.Model):
  __tablename__ = "household"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  members = db.relationship("User", backref="household", lazy=True)
  chores = db.relationship("Chore", 
    secondary=household_chores, 
    lazy="subquery", 
    backref=db.backref("chores"), 
    lazy=True
  )

  def __repr__(self):
    return f"Household {self.name}"
  
class User(db.Model):
  __tablename__ = "user"

  id = db.Column(db.Integer, primary_key=True)
  email = db.Colum(db.String, unique=True, nullable=False)
  name = db.Column(db.String(25), nullable=False)
  household_id = db.Column(db.Integer, db.ForiegnKey("households.id", ondelete="SET NULL"))
  chores = db.relationship("Chore", 
    secondary=household_chores, 
    lazy="subquery", 
    backref=db.backref("chores"), 
    lazy=True
  )

  def __repr__(self):
    return f"User {self.name} has email {self.email} and is in household {self.household_id}"

class Chore(db.Model):
  __tablename__ = "chore"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  description = db.Column(db.String(180))
  difficulty = db.Column(db.Integer, nullable=False)
  