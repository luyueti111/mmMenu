from mmMenu import db
from datetime import datetime


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    introduction = db.Column(db.Text)
    imageUrl = db.Column(db.String)
    lastEdit = db.Column(db.DateTime, default=datetime.now, index=True)
    foods = db.relationship('Food', back_populates='dish')
    isAvailable = db.Column(db.Boolean, default=False)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    quantityDemand = db.Column(db.Float)
    unit = db.Column(db.String)
    isNecessary = db.Column(db.Boolean)
    isAvailable = db.Column(db.Boolean, default=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'))
    dish = db.relationship('Dish', back_populates='foods')


class FoodWeHave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    quantity = db.Column(db.Float)
    unit = db.Column(db.String)