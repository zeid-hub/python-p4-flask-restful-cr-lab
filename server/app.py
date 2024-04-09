#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        my_plants = Plant.query.all()
        my_plant_lists = []
        for plant in my_plants:
            my_plant_lists.append(plant.to_dict())
        response = make_response(
            my_plant_lists,
            200
        )
        return response

    def post(self):
        data = request.get_json() or {}

        new_plant = Plant(name=data["name"], image=data["image"], price=data["price"])
        db.session.add(new_plant)
        db.session.commit()

        response = make_response(
            new_plant.to_dict(),
            200
        )
        return response

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self,id):
        my_specific_plant = Plant.query.filter_by(id=id).first()
        response = make_response(
            my_specific_plant.to_dict(),
            200
        )
        return response

api.add_resource(PlantByID, "/plants/<int:id>")
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
