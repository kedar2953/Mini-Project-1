from app.controllers import blueprint, mongo, jsonify, datetime, resnet, request
from app.schemas import validate_detectionHistory,validate_plant
from bson.objectid import ObjectId
import flask
from flask_cors import CORS, cross_origin
from django.http import JsonResponse
import json
from bson.json_util import loads
import jsonschema

@blueprint.route('/api/dl', methods=["GET"])
def hello():
    return 'Hello, World!'


@blueprint.route('/api/dl/prediction/test', methods=['GET'])
def test1():
    print(ObjectId("623a3d74960a9f8526395e08"))
    data = validate_detectionHistory(
        {"createdAt": str(datetime.now()),
         "plantId": ObjectId("623a3d74960a9f8526395e08")})
    if data['ok']:
        data = data['data']
        print(mongo.db.detectionHistory.find_one())
        print(type(mongo.db.detectionHistory.find_one()['_id']))
        mongo.db.detectionHistory.insert_one(data)
        return jsonify({'ok': True, 'message': 'User created successfully!', 'detectionHistory': data}), 200

    return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@blueprint.route('/api/dl/detection', methods=['POST'])
@cross_origin(supports_credentials=True)
def dl_detection():
    try:
        uid = '124352414'
        city = 'Mumbai'
        ip = '13143536'
        district = 'Mumbai City'
        state = 'MH'
        lat = 11.4652
        lon = 242.24

        # print(request.headers)

        image = request.files['image']
        detection = resnet.predict_image(image)
        detection_split = detection.split('___')

        plant, disease = detection_split[0], detection_split[1]
        # if disease_info is None:
        #     mongo.db.disease.insert_one({})
        print("Detection", plant)

        
        query = {"properties.commonName":plant}
        query2 = {"properties.name":disease}

        disease_document = mongo.db.disease.find_one(query2)

        # Find and validate the document
        plant_document = mongo.db.plants.find_one(query)
        plant_properties = None
        # Validate the document against the schema
        disease_properties = None
        if plant_document:
            try:
                # Validate the document against the schema
                validate_plant(plant_document)
                # print(plant_document)
                plant_properties = plant_document['properties']
                print(plant_properties)
                print("Plant is valid and matches the schema.")
            except Exception as e:
                print(f"Plant does not match the schema: {e}")
        else:
            print("Plant not found.")


        if disease_document:
            try:
                # Validate the document against the schema
                validate_plant(disease_document)
                # print(plant_document)
                disease_properties = disease_document['properties']
                print(disease_properties)
                print("Disease is valid and matches the schema.")
            except Exception as e:
                print(f"Disease does not match the schema: {e}")
        else:
            print("Disease not found.")

        detectionHistory = {
            "createdAt": str(datetime.now()),
            "ip": ip,
            "city": city,
            "district": district,
            "state": state,
            "location": {
                "lat": str(lat),
                "lon": str(lon)
            },
            "detected_class": detection,
            "plantId":1,
            "diseaseId":1 if disease_document == None  else str(disease_document['_id']),
            "rating": 5
        }
        # print(detectionHistory)
        validated_detectionHistory = validate_detectionHistory(detectionHistory)
        dt = json.dumps(validated_detectionHistory)
        done = mongo.db.detectionHistory.insert_one(validated_detectionHistory['data'])
        response = flask.jsonify({'ok': True, 'detection': str(detection),
                                'validated_detectionHistory ': dt, "plant": plant_properties,
                                "disease": "No disease found" if disease_properties == None else disease_properties})

                     
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')

        return response
        return JsonResponse({"message":"hello"})
    #     return jsonify({'ok': True, 'detection': detection,'validated_detectionHistory ':validated_detectionHistory,"plant":plant_info,"disease":"No disease found" if disease_info==None else disease_info}), 200
    except Exception as ex:
        print("error ",ex)
        return flask.jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(ex)}), 500

    # print(ObjectId("623a3d74960a9f8526395e08"))
    # data = validate_detectionHistory({"createdAt":str(datetime.now()),"plantId":ObjectId("623a3d74960a9f8526395e08")})
    # if data['ok']:
    #     data = data['data']
    #     print(mongo.db.detectionHistory.find_one())
    #     print(type(mongo.db.detectionHistory.find_one()['_id']))
    #     mongo.db.detectionHistory.insert_one(data)
    #     return jsonify({'ok': True, 'message': 'User created successfully!','detectionHistory':data}), 200
