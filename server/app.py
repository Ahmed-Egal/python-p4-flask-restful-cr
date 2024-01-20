#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        return {"msg" : "Hello "}
    
api.add_resource(Home, '/')



class Newsletter(Resource):
    def get(self):
        response_dict = [n.to_dict() for n in Newsletter.query.all()]

        response = make_response(jsonify(response_dict), 200)
        return response
    

    def post(self):
        new_record = Newsletter(
            title = request.form['title'],
            body = request.form['body'],)
        
        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()
        response = make_response(
            jsonify(response_dict), 201
        )

        return response


api.add_resource(Newsletter, '/newsletter')


class NewsletterById(Resource):
    def get(self, id):
        res_dict = Newsletter.query.filter_by(id=id).first().to_dict()

        response = make_response(jsonify(res_dict), 200)

        return response
    
api.add_resource(NewsletterById, '/newsletter/<int:id>')












class Newsletter(db.Model, SerializerMixin):
    __tablename__ = 'newsletters'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    published_at = db.Column(db.DateTime, server_default=db.func.now())
    edited_at = db.Column(db.DateTime, onupdate=db.func.now())




if __name__ == '__main__':
    app.run(port=5555, debug=True)
