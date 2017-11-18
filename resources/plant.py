# copied from item.py
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.plant import PlantModel

class Plant(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('quantity',
						type=float,
						required=True,
						help="This field cannot be left blank!")

	parser.add_argument('price',
						type=float,
						required=True,
						help="This field cannot be left blank!")

	parser.add_argument('genus_name',
						type=str,
						required=True,
						help="Every plant needs a genus name")

	@jwt_required()
	def get(self, name):
		plant = PlantModel.find_by_name(name)
		if plant:
			return plant.json()
		return {"message": "Plant not found"}, 404

	@jwt_required()
	def post(self, name):
		if PlantModel.find_by_name(name):
			return {'message': 'An plant with name "{}" already exists'.format(name)}, 400 # 400 means bad request

		# Makes sure the item json the user sends to us has a price field.
		data = Plant.parser.parse_args()
		plant = PlantModel(name, data['quantity'], data['price'], data['genus_name'])
		# Try and insert the POST data into the database.
		try:
			plant.save_to_db()
		except:
			return {"message": "An error occurred inserting the plant."}, 500 # Internal Server Error

		return plant.json(), 201

	@jwt_required()
	def put(self, name):
		data = Plant.parser.parse_args()
		plant = PlantModel.find_by_name(name)

		if plant is None:
			plant = PlantModel(name, data['quantity'], data['price'], data['genus_name'])
		else:
			plant.quantity = data['quantity']
			plant.price = data['price']
		plant.save_to_db()

		return plant.json()

	@jwt_required()
	def delete(self, name):
		plant = PlantModel.find_by_name(name)
		if plant:
			plant.delete_from_db()

		return {"message": "Plant deleted"}


class PlantList(Resource):
	def get(self):
		return {'plant': [plant.json() for plant in PlantModel.query.all()]}
