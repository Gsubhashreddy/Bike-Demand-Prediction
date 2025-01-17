import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import seaborn as sns  
import pickle
import model
import math

app= Flask(__name__, static_url_path='/static')
my_model=pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def shuffle():
    return render_template('index.html')

@app.route('/shuffle')
def predictionpage():
    return render_template('shuffle.html')

@app.route('/predict', methods=['POST'])
def predict():

#fetching the input values
    input_values = [float(i) for i in request.form.values()]  
 #This will form the input row    
    df_row=[[i] for i in input_values]
#fetching the input keys                       
    df_keys = [i for i in request.form.keys()]   
#declaring list of keys which has to be rescaled 
    rescaling_cols=['temp', 'hum', 'windspeed']          

    #Declaring dictionary to convert into dataframe in the next step.
    html_dict = {df_keys[i]: df_row[i] for i in range(len(df_keys))}

    def creating_input_to_model(dict):
        df_dict = {}
        if dict['weather']==[1.0]:
            df_dict['Best']=[1.0]
            df_dict['Neutral']=[0.0]
        elif dict['weather']==[2.0]:
            df_dict['Best']=[0.0]
            df_dict['Neutral']=[1.0]
        else:
            df_dict['Best'] = [0.0]
            df_dict['Neutral'] = [0.0]

        if dict['Seasons']==[1.0]:
            df_dict['spring']=[1.0]
            df_dict['temp']=dict['temp']
        else:
            df_dict['spring'] = [0.0]
            df_dict['temp'] = dict['temp']

        if dict['Seasons']==[4.0]:
            df_dict['winter']=[1.0]
            df_dict['summer']=[0.0]
        elif dict['Seasons']==[2.0]:
            df_dict['winter'] = [0.0]
            df_dict['summer'] = [1.0]
        else:
            df_dict['winter'] = [0.0]
            df_dict['summer'] = [0.0]

        df_dict['hum']=dict['hum']

        if dict['Month']==[7.0]:
            df_dict['Jul']=[1.0]
            df_dict['Sep']=[0.0]
        elif dict['Month']==[9.0]:
            df_dict['Jul'] = [0.0]
            df_dict['Sep'] = [1.0]
        else:
            df_dict['Jul'] = [0.0]
            df_dict['Sep'] = [0.0]

        df_dict['windspeed'] = dict['windspeed']
        df_dict['yr']= dict['yr']
        df_dict['holiday']=dict['holiday']
        print(df_dict)
        return df_dict

    func_dict=creating_input_to_model(html_dict)
    df=pd.DataFrame(func_dict)
    df[df.columns[df.columns.isin(rescaling_cols)]] = model.scaler.transform(df[df.columns[df.columns.isin(rescaling_cols)]])

    #Prediction of the trained model
    prediction= my_model.predict(df)
    #Output derived from the ML model
    output= math.ceil(prediction[0])

    #Output sent to the html page
    return render_template('index.html', prediction_text='Prediction: \n {} bikes are needed.'.format(output))

if __name__=="__main__":
    app.run(debug=True)