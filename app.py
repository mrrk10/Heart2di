from curses import use_default_colors
import imp
from tkinter.messagebox import RETRY
from tokenize import String
from flask import Flask, render_template, url_for, flash, redirect
import joblib
from flask import request, jsonify
import numpy as np

app = Flask(__name__, template_folder='templates')




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")    
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template('login.html')    
@app.route("/register")
def register():
    return render_template('register.html') 

       
#######################################################################################
#LOGISTIC REGRESSION

def ValuePredictor(to_predict_list, size, algo):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==7):
        loaded_model = joblib.load(algo)
        result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/predict1', methods = ["POST"])
def predict():
    prediction=""
    if request.method == "POST":

        form = request.form.to_dict()
        predict1 = predict2 = None
        if 'predict1' in form:
            predict1 = form['predict1'] or None
            del form['predict1']
        
        if 'predict2' in form:
            predict2= form['predict2'] or None
            del form['predict2']

        to_predict_list = list(form.values())
        to_predict_list = list(map(float,to_predict_list))
        
        result = ""
        accuracy=""
        if predict1:
            if(len(to_predict_list)==7):
                result = ValuePredictor(to_predict_list,7,'hdp_model.pkl')
                accuracy = "Predict 1"
        elif predict2:
            if(len(to_predict_list)==7):
                result = ValuePredictor(to_predict_list,7,'randomf_model.pkl')
                accuracy = "Predict 2"

        if(int(result)==1):
            prediction = "You have heart condition, Consult the doctor immediately"
        else:
            prediction = "You are safe. You have no dangerous symptoms !!! :-)"
    return(render_template("prediction_result.html", prediction_text=prediction,accuracy=accuracy))       

@app.route('/api/predict/', methods = ["POST"])
def predict_api():
    prediction=""
    if request.method == "POST":

        form = request.json.to_dict()
        predict1 = predict2 = None
        if 'predict1' in form:
            predict1 = form['predict1'] or None
            del form['predict1']
        
        if 'predict2' in form:
            predict2= form['predict2'] or None
            del form['predict2']

        to_predict_list = list(form.values())
        to_predict_list = list(map(float,to_predict_list))
        
        result = ""
        accuracy=""
        if predict1:
            if(len(to_predict_list)==7):
                result = ValuePredictor(to_predict_list,7,'hdp_model.pkl')
                accuracy = "Predict 1"
        elif predict2:
            if(len(to_predict_list)==7):
                result = ValuePredictor(to_predict_list,7,'randomf_model.pkl')
                accuracy = "Predict 2"

        if(int(result)==1):
            prediction = "You have heart condition, Consult the doctor immediately"
        else:
            prediction = "You are safe. You have no dangerous symptoms !!! :-)"
    return jsonify({'status': True,"prediction":prediction,"accuracy":accuracy})  

######################################################################################################   
##RANDOM FOREST###
def testpredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==7):
        loaded_model = joblib.load('random_model.pkl')
        result_t= loaded_model.predict(to_predict)
    return result_t[0]


@app.route('/predict2', methods = ["POST"])
def test():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        
        if(len(to_predict_list)==7):
            result = ValuePredictor(to_predict_list,7)
    
    if(int(result)==1):
        prediction = "You have heart condition, Consult the doctor immediately"
    else:
        prediction = "You are safe. You have no dangerous symptoms !!! :-)"
    return(render_template("prediction_result.html", prediction_text=prediction))       






####################################################################################################
if __name__ == "__main__":
    # Use below for local flask deployment
    app.run(debug=True,port=5001)
    
    #Use below for AWS EC2 deployment
    #app.run(host='0.0.0.0',port=8081)
