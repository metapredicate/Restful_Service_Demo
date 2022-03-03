from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from other_class import OtherClass
import os

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class DemoResource(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(80), unique = True) #, nullable=False)
    email = db.Column(db.String(120)) #, nullable=False)

    def __init__(self, user_name, email):
        self.user_name = user_name
        self.email = email

class DemoResourceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_name', 'email')

demo_resource_schema = DemoResourceSchema()
demo_resources_schema = DemoResourceSchema(many=True)


@app.route("/", methods=['GET'])
def hello() -> str:
    """
    TODO: _summary_
    """
    return "Hello World"

@app.route("/endpoints/1/", methods=["GET"])
def my_func():
    bob = ["1","2","3"]
    return jsonify(bob)

@app.route('/demoresource', methods=['POST'])
def add_resource():
    user_name = request.json['user_name']
    app.logger.info(f'user_name := {user_name}')
    email = request.json['email']
    app.logger.info(f'email := {email}')

    new_resource = DemoResource(user_name, email)

    db.session.add(new_resource)
    db.session.commit()

    return demo_resource_schema.jsonify(new_resource)

@app.route('/demoresource/<id>', methods=['GET'])
def get_demoresource(id):
    demoresource = DemoResource.query.get(id)
    return demo_resource_schema.jsonify(demoresource)


@app.route('/demoresource', methods=['GET'])
def get_all_demoresources():
    demoresources = DemoResource.query.all()
    result = demo_resources_schema.dump(demoresources)
    return jsonify(result)

@app.route('/demoresource/<id>', methods=['PUT'])
def update_resource(id):
    resource = DemoResource.query.get(id)
    user_name = request.json['user_name']
    app.logger.info(f'user_name := {user_name}')
    email = request.json['email']
    app.logger.info(f'email := {email}')

    resource.user_name = user_name
    resource.email = email
    db.session.commit()
    return demo_resource_schema.jsonify(resource)

@app.route('/demoresource/<id>', methods=['DELETE'])
def delete_resource(id):
    resource = DemoResource.query.get(id)
    db.session.delete(resource)
    db.session.commit()
    return demo_resource_schema.jsonify(resource)

if __name__ == '__main__':
    app.run()
