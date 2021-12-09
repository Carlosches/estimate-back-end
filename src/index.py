from HouseEncoder import HouseEncoder
from json import decoder
from flask import Flask, render_template, request,jsonify, Blueprint
from flask_cors import CORS
import json
import predictor
import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("venv/services.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)
price = 0

CORS(app)
# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/about')
# def about():
#     return render_template("about.html")

@app.route('/predict', methods=['POST'])
def predict():
    property = request.get_json()
    area= property['area']
    rooms= property['rooms']
    bathrooms= property['bathrooms']
    garages= property['garages']
    sel= property['sel']
    lon= property['longitude']
    lan= property['latitude']
    userId= property['userId']
    price = predictor.prediction(area,rooms,bathrooms,garages,sel,lon,lan)
    price_predicted = {'price': price}
    savePrediction(area,rooms,bathrooms,garages,sel,lon,lan, price,userId)
    return jsonify(price_predicted)



def savePrediction(area,rooms,bathrooms,garages,sel,lon,lan, result,userId):
    db.collection(u'users').document(userId).update({  
      "Predictions":firestore.ArrayUnion([{
              "area": area,
                "rooms":rooms,
                "bathrooms":bathrooms,
                "garages":garages,
                "sel":sel,
                "lon":lon,
                "lan":lan,
                "result":result
      }])
    })
  
        
@app.route('/predictions', methods=['GET'])
def getPredictions():   
    userId=request.args.get('userId')
    doc_ref = db.collection(u'users').document(userId)
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
    else:
        print(u'No such document!')

@app.route('/houses', methods=['GET', 'POST'])
def nearHouses():
    if request.method == 'POST':
        property = request.get_json()
        
        lon= property['longitude']
        lan= property['latitude']
        print(lon, " ", lan)
        houses = predictor.getNearHouses(lon,lan)

        #print("houses: ", houses)
        result = {'houses': houses}
    
        return jsonify(result)

    
if(__name__ == '__main__'):
    app.run(debug=True)
