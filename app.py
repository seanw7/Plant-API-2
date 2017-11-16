from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.plant import Plant, PlantList
from resources.genus import Genus, GenusList


import json
import os

# searches os envvars for "VCAP_SERVICES"
vcap_config = os.getenv('VCAP_SERVICES', "")
decoded_config = json.loads(vcap_config)

# locate the cloudfoundry environment variables json
mysql_creds = decoded_config['p-mysql'][0]['credentials']
print(mysql_creds)

# target and extract the mysql db uri
raw_uri = str(mysql_creds['uri'])
db_uri = raw_uri.strip('?reconnect=true')
print(db_uri)

# initialize flask app
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost:3306/my-test-db-1'#?reconnect=true' # Works for local pcfdev
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'testKey'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth  end point

api.add_resource(Genus, '/genus/<string:name>')
api.add_resource(Plant, '/plant/<string:name>')
api.add_resource(PlantList, '/plants')
api.add_resource(UserRegister, '/register')
api.add_resource(GenusList, '/genera')


if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True)
