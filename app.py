from flask import Flask, render_template, request
import requests
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('model/xgb.pkl', 'rb'))


@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    Year_buy = int(request.form['Year'])
    Present_Price = int(request.form['Present_Price'])
    Kms_Driven = int(request.form['Kms_Driven'])
    brand = request.form['brand']
    Engine = int(request.form['Engine'])
    Power = int(request.form['Power'])
    Mileage = int(request.form['Mileage'])
    Seats = int(request.form['Seats'])
    Kms_Driven2 = np.log(Kms_Driven)
    Owner = int(request.form['Owner'])
    Fuel_Type = request.form['Fuel_Type_Petrol']
    if(Fuel_Type == 'Petrol'):
        Fuel_Type_Petrol = 1
        Fuel_Type_Diesel = 0
    else:
        Fuel_Type_Petrol = 0
        Fuel_Type_Diesel = 1
    Year = 2022-Year_buy
    Seller_Type_Individual = 1
    Transmission = request.form['Transmission_Mannual']
    if(Transmission == 'Mannual'):
        Transmission_Mannual = 1
    else:
        Transmission_Mannual = 0
    prediction = model.predict([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel,
                               Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]])
    output = round(prediction[0], 2)
    print(output)
    if output < 0:
        return render_template('result.html', prediction_texts="Sorry you cannot sell this car", Price=Present_Price, Year=Year_buy, Kms_Driven=Kms_Driven, brand=brand, Engine=Engine, Power=Power, Mileage=Mileage, Seats=Seats, Transmission=Transmission, Owners=Owner, Fuel_type=Fuel_Type)
    else:
        return render_template('result.html', prediction_text="You Can Sell The Car at {}".format(output), Price=Present_Price, Year=Year_buy, Kms_Driven=Kms_Driven, brand=brand, Engine=Engine, Power=Power, Mileage=Mileage, Seats=Seats, Transmission=Transmission, Owners=Owner, Fuel_type=Fuel_Type)


if __name__ == "__main__":
    app.run(debug=True)