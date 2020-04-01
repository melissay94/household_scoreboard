from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost/household_scoreboard"

db = SQLAlchemy(app)

household_chores = db.Table("household_chores",
  db.Column("household_id", db.Integer, db.ForeignKey("households.id"), primary_key=True),
  db.Column("chore_id", db.Integer, db.ForeignKey("chores.id"), primary_key=True),
  db.Column("completed", db.Boolean, default=False)
)

user_chores = db.Table("pending_user_chores",
  db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
  db.Column("chore_id", db.Integer, db.ForeignKey("chores.id"), primary_key=True),
  db.Column("completed", db.Boolean, default=False)
)

class Household(db.Model):
  __tablename__ = "households"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  members = db.relationship("User", backref="household", lazy=True)
  chores = db.relationship("Chore", 
    secondary=household_chores, 
    lazy="subquery", 
    backref=db.backref("household_chores")
  )

  def __repr__(self):
    return f"Household {self.name}"
  
class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, unique=True, nullable=False)
  name = db.Column(db.String(25), nullable=False)
  score = db.Column(db.Integer, nullable=False, default=0)
  household_id = db.Column(db.Integer, db.ForeignKey("households.id", ondelete="SET NULL"))
  chores = db.relationship("Chore", 
    secondary=user_chores, 
    lazy="subquery", 
    backref=db.backref("user_chores")
  )

  def __repr__(self):
    return f"User {self.name} has email {self.email} and is in household {self.household_id}"

class Chore(db.Model):
  __tablename__ = "chores"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  description = db.Column(db.String(180))
  difficulty = db.Column(db.Integer, nullable=False)

  def __repr__(self):
    return f"Chore {self.name} is {self.description} and has a {self.difficulty} rating"

