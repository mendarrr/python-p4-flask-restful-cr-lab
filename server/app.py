from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from models import db, Plant
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return [plant.to_dict() for plant in plants]

    def post(self):
        data = request.get_json()
        plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(plant)
        db.session.commit()
        return plant.to_dict(), 201

class PlantById(Resource):
    def get(self, id):
        plant = db.session.get(Plant, id)
        if plant:
            return plant.to_dict()
        return {'message': 'Plant not found'}, 404

api.add_resource(Plants, '/plants')
api.add_resource(PlantById, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
