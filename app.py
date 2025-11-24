import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.5
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
# Keras
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template,session,flash,redirect, url_for, session,flash
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
# Define a flask app
app = Flask(__name__)
app.secret_key = '1a2b3c4d5e'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'account'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
                # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            #session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return render_template('index.html',title="Plant")#redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password!", "danger")
    return render_template('login.html',title="Login")



@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        cursor.execute( "SELECT * FROM accounts WHERE username LIKE %s", [username] )
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash("Account already exists!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash("Username must contain only characters and numbers!", "danger")
        elif not username or not password or not email:
            flash("Incorrect username/password!", "danger")
        else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s)', (username,email, password))
            mysql.connection.commit()
            flash("You have successfully registered!", "success")
            return render_template('login.html',title="Login")

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!", "danger")
    # Show registration form with message (if any)
    return render_template('login.html',title="Register")
# Model saved with Keras model.save()
MODEL_PATH ='bone.h5'

# Load your trained model
model = load_model(MODEL_PATH)




def model_predict(img_path, model):
    print(img_path)
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
   # x = preprocess_input(x)

    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    p1=model.predict(x)[0][0]*100
    print(p1)
    
    if preds==0:
        
        p1=round(model.predict(x)[0][0]*100,2)
        print(p1)
        preds="Avulsion fracture" +" with accuracy "+str(p1)+"%"

    elif preds==1:
        p1=round(model.predict(x)[0][1]*100,2)
        
        preds="Comminuted fracture"+" with accuracy "+str(p1)+"%"
        
    elif preds==2:
        p1=round(model.predict(x)[0][2]*100,2)
        
        preds="Compression-Crush fracture"+" with accuracy "+str(p1)+"%"
        
    elif preds==3:
        p1=round(model.predict(x)[0][3]*100,2)
        
        preds="Fracture Dislocation"+" with accuracy "+str(p1)+"%"
        
    elif preds==4:
        p1=round(model.predict(x)[0][4]*100,2)
        
        preds="Greenstick fracture"+" with accuracy "+str(p1)+"%"
        
    elif preds==5:
        p1=round(model.predict(x)[0][5]*100,2)
        preds="Hairline Fracture"+" with accuracy "+str(p1)+"%"
        
    elif preds==6:
        p1=round(model.predict(x)[0][6]*100,2)
        preds="Impacted fracture"+" with accuracy "+str(p1)+"%"
        
    elif preds==7:
        p1=round(model.predict(x)[0][6]*100,2)
        preds="Intra-articular fracture"+" with accuracy "+str(p1)+"%"
    elif preds==8:
        p1=round(model.predict(x)[0][6]*100,2)
        preds="Longitudinal  fracture"+" with accuracy "+str(p1)+"%"
    elif preds==9:
        p1=round(model.predict(x)[0][6]*100,2)
        preds="Oblique  fracture"+" with accuracy "+str(p1)+"%"
    elif preds==10:
        p1=round(model.predict(x)[0][6]*100,2)
        preds="Pathological   fracture"+" with accuracy "+str(p1)+"%"
    elif preds==11:
        p1=round(model.predict(x)[0][6]*100,2)
        preds="Spiral  fracture"+" with accuracy "+str(p1)+"%"
        

    
    
    return (preds)


@app.route('/home', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        pred= model_predict(file_path, model)
        result=pred
        #emails(result,file_path)
        return (result)
    return None


if __name__ == '__main__':
    app.run(port=5001,debug=True)
