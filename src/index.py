from HouseEncoder import HouseEncoder
from json import decoder
from flask import Flask, render_template, request,jsonify
import json
import predictor

app = Flask(__name__)
price = 0

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/about')
# def about():
#     return render_template("about.html")

@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        property = request.get_json()
        area= property['area']
        rooms= property['rooms']
        bathrooms= property['bathrooms']
        garages= property['garages']
        sel= property['sel']
        lon= property['longitude']
        lan= property['latitude']

        price = predictor.prediction(area,rooms,bathrooms,garages,sel,lon,lan)
        price_predicted = {'price': price}
        return jsonify(price_predicted)

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
