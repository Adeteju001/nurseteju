#!/usr/bin/env python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template, url_for, request, redirect
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
from datetime import datetime


app = Flask(__name__)


#Create a connection and a database
dbase = pymysql.connections.Connection(
        host='localhost',
        user='adesina',
        password='ab702810'
        )

print (dbase)

cursor = dbase.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS nurseteju_db")
cursor.execute("USE nurseteju_db")



#Configuring the Flask app to connect to the MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://adesina:ab702810@localhost/nurseteju_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Creating an instance of the SQLAlchemy class
db = SQLAlchemy(app)


main = Blueprint('main', __name__)
main_blueprint = main
app.register_blueprint(main_blueprint)


#create the database table
class Member(db.Model):
    
    ID = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date, default=datetime.utcnow)
    Full_Name = db.Column(db.VARCHAR(100))
    Sex = db.Column(db.VARCHAR(100))
    Age = db.Column(db.VARCHAR(100))
    Marital_Status = db.Column(db.VARCHAR(100))
    Address = db.Column(db.VARCHAR(100))
    Phone_Number = db.Column(db.VARCHAR(100))
    Temperature = db.Column(db.VARCHAR(100))
    Blood_Pressure = db.Column(db.VARCHAR(100))
    Weight = db.Column(db.VARCHAR(100))
    Symptom = db.Column(db.VARCHAR(100))
    Assigned_Doctor = db.Column(db.VARCHAR(100))
    Admission_Status = db.Column(db.VARCHAR(100))


def save_to_drive():
    engine = create_engine('mysql+pymysql://adesina:ab702810@localhost/nurseteju_db')
    query = """SELECT * FROM member;"""
    df = pd.read_sql(query, engine)
    df_csv = df.to_csv('nurseteju_db.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_info')
def new_info():
    return render_template('new_info.html')

@app.route('/new_info_post', methods=["GET", "POST"])
def new_info_post():

    #Assign from HTML to python
    full_name_py = request.form.get('full_name_html')
    sex_py = request.form.get('sex_html')
    age_py = request.form.get('age_html')
    marital_status_py = request.form.get('marital_status_html')
    address_py = request.form.get('address_html')
    phone_number_py = request.form.get('phone_number_html')
    temperature_py = request.form.get('temperature_html')
    blood_pressure_py = request.form.get('blood_pressure_html')
    weight_py = request.form.get('weight_html')
    symptom_py = request.form.get('symptom_html')
    assigned_doctor_py = request.form.get('assigned_doctor_html')
    admission_status_py = request.form.get('admission_status_html')

    #create a new user, that is, to allocate a row to store the information.

    print (f"My name is: {full_name_py}")
    engine = create_engine('mysql+pymysql://adesina:ab702810@localhost/nurseteju_db')

    new_user = Member(
            Full_Name = full_name_py,
            Sex = sex_py,
            Age = age_py,
            Marital_Status = marital_status_py,
            Address = address_py,
            Phone_Number = phone_number_py,
            Temperature = temperature_py,
            Blood_Pressure = blood_pressure_py,
            Weight = weight_py,
            Symptom = symptom_py,
            Assigned_Doctor = assigned_doctor_py,
            Admission_Status = admission_status_py
            )

    db.session.add(new_user)
    db.session.commit()


    #copy the database to a csv file
    save_to_drive()
    return redirect(url_for('index'))

@app.route('/show_data')
def show_data():
    return render_template('show_data.html')

@app.route('/pre_show_data')
def pre_show_data():
    engine = create_engine('mysql+pymysql://adesina:ab702810@localhost/nurseteju_db')
    query = """SELECT * FROM member;"""
    df = pd.read_sql(query, engine)
    #df = pd.read_sql_table('member', engine)
    save_to_drive()
    return (df.to_html())


@app.route('/search_data')
def search_data():
    return render_template('search_data.html')

@app.route('/search_data_column', methods=["GET", "POST"])
def search_data_column():
    search_data_py = request.form.get('search_column_html')
    engine = create_engine('mysql+pymysql://adesina:ab702810@localhost/nurseteju_db')
    df = pd.read_sql_table('member', engine, columns=[f'{search_data_py}'])
    return (df.to_html())

@app.route('/search_data_row', methods=["GET", "POST"])
def search_data_row():
    search_column_py = request.form.get('search_column_row_html')
    search_row_py = request.form.get('search_row_html')
    engine = create_engine('mysql+pymysql://adesina:ab702810@localhost/nurseteju_db')
    query = f"SELECT * FROM member WHERE {search_column_py} LIKE '{search_row_py}'"
    df = pd.read_sql(query, engine)
    return (df.to_html())

@app.route('/edit_data')
def edit_data():
    return render_template('edit_data.html')

@app.route('/edit_data_post', methods=["GET", "POST"])
def edit_data_post():
    edit_move_py = request.form.get('edit_move_html')
    edit_after_py = request.form.get('edit_after_html')
    query = f"ALTER TABLE member MODIFY {edit_move_py} VARCHAR(100) AFTER {edit_after_py}"
    cursor.execute(query)
    dbase.commit()
    #copy the database to a csv file
    save_to_drive()
    return redirect(url_for('pre_show_data'))

@app.route('/update_data_post', methods=["GET", "POST"])
def update_data_post():
    update_select_column_py = request.form.get('update_select_column_html')
    update_search_id_py = request.form.get('update_search_id_html')
    update_text_py = request.form.get('update_text_html')
    query = f"UPDATE member SET {update_select_column_py} = '{update_text_py}' WHERE ID = {update_search_id_py}"
    cursor.execute(query)
    dbase.commit()

    #copy the database to a csv file
    save_to_drive()
    return redirect(url_for('pre_show_data'))




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
    cursor.close()
    dbase.close()

