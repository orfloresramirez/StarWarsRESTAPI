"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Vehicles, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_all_users():


    results = User.query.all()
    results_map = list(map(lambda item: item.serialize(), results ))
    response_body = {
        "msg": "ok",
        "results": results_map
    }

    return jsonify(response_body), 200


@app.route('/characters', methods=['GET'])
def get_all_characters():

    results = Characters.query.all()
    # print(results)
    results_map = list(map(lambda item: item.serialize(), results ))
    # print(results_map)
    response_body = {
        "msg": "ok",
        "results": results_map
    }

    return jsonify(response_body), 200


@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():

    results = Vehicles.query.all()
    # print(results)
    results_map = list(map(lambda item: item.serialize(), results ))
    # print(results_map)
    response_body = {
        "msg": "ok",
        "results": results_map
    }

    return jsonify(response_body), 200



@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):

    try:       
        result = Characters.query.filter_by(id=character_id).first()
        response_body = {
            "msg": "ok",
            "result": result.serialize()
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({"error": "error en servidor"+str(e)}), 500
    

@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_favorites_by_user(user_id):
    try: 
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "user not exist"}), 404

        result = Favorites.query.filter_by(user_id=user_id).all()
        print(list(result))
        result_map = list(map(lambda item: item.serialize(), result ))
        print(result_map)
        response_body = {
            "msg": "ok",
            "result": result_map
        }

        return jsonify(response_body), 200
    
    except Exception as e:
        return jsonify({"error": "error en servidor "+str(e)}), 500


@app.route('/users/favorites/characters/<int:character_id>', methods=['POST'])
def add_character(character_id):
    try:
        character = Characters.query.get(character_id)
        verif_favorite = Favorites.query.filter_by(character_id=character.id).first()
        # print(verif_favorite)
        if verif_favorite:
            return jsonify({"error": "character already exist in Favorites list"}), 404

        if not character:
            return jsonify({"error": "character not exist"}), 404

        body = request.get_json(force=True)

        new  = Favorites(
            user_id= body["user_id"],
            character_id= character_id
        )

        user = User.query.get(body["user_id"])
        if not user:
            return jsonify({"error": "user not exist"}), 404

        
        db.session.add(new)
        db.session.commit()


        return jsonify({"done":"item added: "+character.name}), 200
    except Exception as e:
        return jsonify({"error": "error en servidor "+str(e)}), 500

@app.route('/users/favorites/vehicles/<int:vehicle_id>', methods=['POST'])
def add_vehicle(vehicle_id):
    try:
        vehicle = Vehicles.query.get(vehicle_id)
        verif_favorite = Favorites.query.filter_by(vehicle_id=vehicle.id).first()
        # print(verif_favorite)
        if verif_favorite:
            return jsonify({"error": "vehicle already exist in Favorites list"}), 404


        if not vehicle:
            return jsonify({"error": "vehicle not exist"}), 404
    

        body = request.get_json(force=True)

        new  = Favorites(
            user_id= body["user_id"],
            vehicle_id= vehicle_id
        )

        user = User.query.get(body["user_id"])
        if not user:
            return jsonify({"error": "user not exist"}), 404

        db.session.add(new)
        db.session.commit()


        return jsonify({"done":"item added: "+vehicle.name}), 200

    except Exception as e:
        return jsonify({"error": "error en servidor "+str(e)}), 500

@app.route('/users/favorites/planets/<int:planet_id>', methods=['POST'])
def add_planet(planet_id):

    try:
        planet = Planets.query.get(planet_id)

        verif_favorite = Favorites.query.filter_by(planet_id=planet.id).first()
        # print(verif_favorite)
        if verif_favorite:
            return jsonify({"error": "character already exist in Favorites list"}), 404


        if not planet:
            return jsonify({"error": "planet not exist"}), 404
        

        body = request.get_json(force=True)

        new  = Favorites(
            user_id= body["user_id"],
            planet_id= planet_id
        )

        user = User.query.get(body["user_id"])
        if not user:
            return jsonify({"error": "user not exist"}), 404
            
        db.session.add(new)
        db.session.commit()

        return jsonify({"done":"item added: "+planet.name}), 200

    except Exception as e:
        return jsonify({"error": "error en servidor "+str(e)}), 500

@app.route('/users/favorites/characters/<int:character_id>', methods=['DELETE'])
def remove_character(character_id):
    
    try:
        character = Characters.query.get(character_id)
        if not character:
            return jsonify({"error": "character not exist"}), 404    

        body = request.get_json()
        user_id = body["user_id"]

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "user not exist"}), 404

        delete_character = Favorites.query.filter_by(user_id=user_id, character_id=character_id).first()

        db.session.delete(delete_character)
        db.session.commit()

        return jsonify({"done":"item removed: "+character.name}), 200

    except Exception as e:
        return jsonify({"error": "error in server "+str(e)}), 500

@app.route('/users/favorites/vehicles/<int:vehicle_id>', methods=['DELETE'])
def remove_vehicle(vehicle_id):

    try:
        vehicle = Vehicles.query.get(vehicle_id)
        if not vehicle:
            return jsonify({"error": "vehicle not exist"}), 404    

        body = request.get_json()
        user_id = body["user_id"]

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "user not exist"}), 404

        delete_vehicle = Favorites.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()

        db.session.delete(delete_vehicle)
        db.session.commit()

        return jsonify({"done":"item removed: "+vehicle.name}), 200

    except Exception as e:
        return jsonify({"error": "error in server "+str(e)}), 500

@app.route('/users/favorites/planets/<int:planet_id>', methods=['DELETE'])
def remove_planet(planet_id):

    try:
        planet = Planets.query.get(planet_id)
        if not planet:
            return jsonify({"error": "planet not exist"}), 404    

        body = request.get_json()
        user_id = body["user_id"]

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "user not exist"}), 404

        delete_planet = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()

        db.session.delete(delete_planet)
        db.session.commit()

        return jsonify({"done":"item removed: "+planet.name}), 200

    except Exception as e:
        return jsonify({"error": "error in server "+str(e)}), 500
    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
