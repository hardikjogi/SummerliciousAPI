from flask import Flask, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_cors import CORS, cross_origin

# Create a engine for connecting to SQLite3.
# Assuming summer.db is in your app root folder

e = create_engine('sqlite:///summer.db')

app = Flask(__name__)
api = Api(app)
CORS(app, support_credentials=True)

@app.route("/login")
@cross_origin(supports_credentials=True)
def login():
  return jsonify({'success': 'ok'})


app.route('summer', methods=['GET'])
def yourMethod(params):
    response = Flask.jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response






@app.route('/')
def index():
    return '<h4>Summerlicious API End Points. Put /summer in url to get all data or /summer/Itailian to get data by cuisine</h4>'

# description.


class All_Data(Resource):
    def get(self):
        # Connect to database
        conn = e.connect()
        # Perform query and return JSON data
        query = conn.execute("select *  from data")
        #return {'departments': [i[0] for i in query.cursor.fetchall()]}
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return result

class Cuisine(Resource):
    def get(self):
        #Connect to database
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select distinct businesses_categories_title from data")
        return {'departments': [i[0] for i in query.cursor.fetchall()]}

class CuisineFilter(Resource):
    def get(self, department_name):
        conn = e.connect()
        query = conn.execute("select * from data where businesses_categories_title=?", (department_name,))


        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
        #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient

api.add_resource(CuisineFilter, '/summer/<string:department_name>')
api.add_resource(All_Data, '/summer')
api.add_resource(Cuisine, '/summer/cuisine_list')

if __name__ == '__main__':
    app.run()
