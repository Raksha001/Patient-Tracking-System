from app import app, forbidden, internal_server_error
from flask import jsonify, request, redirect
from db_config import mysql
import os
from werkzeug.utils import secure_filename
import datetime
import random

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/fileupload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return filepath

def sql_database(sql_query):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        row = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return row
    except Exception as e:
        print(e)

@app.route('/register',methods=['POST'])
def register():
    try:
        _form = request.form
        _name = _form['name']
        _address = _form['address']
        _phoneNumber = _form['phoneNumber']
        _concern = _form['concern']
        _durationOfTreatment = _form['durationOfTreatment']
        _startDateOfTreatment = _form['startDateOfTreatment']
        _doctorInCharge = _form['doctorInCharge']
        xray = upload_file()
        design = upload_file()
        username = _name
        randomnum = random.randrange(10,99)
        password = f'{username}@{randomnum}'
        _startDateOfTreatment = datetime.datetime.strptime(_startDateOfTreatment, '%Y-%m-%d')

        if _name and _address and _phoneNumber and _concern and _durationOfTreatment and _startDateOfTreatment and _doctorInCharge and xray and design:
        #if _name and _address and _phoneNumber and _concern and _durationOfTreatment and _startDateOfTreatment and _doctorInCharge:
            lastModified = datetime.datetime.now()
            sqlQuery = f"INSERT INTO users (username,password) VALUES ('{username}','{password}')"
            sql_database(sqlQuery)
            sqlQuery = f"SELECT uid FROM users WHERE username='{username}'"
            uid = sql_database(sqlQuery)
            print(uid[0])
            sqlQuery = f"INSERT INTO patientDetails (uid, patientName, address, phoneNumber, concern, durationOfTreatment, startDateOfTreatment, doctorInCharge, xray, designFile, lastModified) VALUES ('{uid}','{_name}', '{_address}', '{_phoneNumber}', '{_concern}', '{_durationOfTreatment}', '{_startDateOfTreatment}', '{_doctorInCharge}', '{_xray}', '{_designFile}', '{lastModified}')"
            #sqlQuery = f"INSERT INTO patient_details (uid, patientName, address, phoneNumber, concern, durationOfTreatment, startDateOfTreatment,doctorInCharge, lastModified) VALUES ('{uid[0]}','{_name}', '{_address}', '{_phoneNumber}', '{_concern}', '{_durationOfTreatment}','{_startDateOfTreatment}', '{_doctorInCharge}', '{lastModified}')"
            sql_database(sqlQuery)
            return {'status': 'success'}
        else:
            return {'status': 'false'}
    except Exception as e:
        return internal_server_error()

@app.route('/user', methods=['PUT','DELETE'])
def edituser():
    if request.method =='PUT':
        try:
            _uid = request.json["uid"]
            _token = request.json["token"]
            if _token:
                sqlQuery = f"SELECT isAdmin FROM users WHERE uid='{_uid}' and '{_token}'"
                isAdmin = sql_database(sqlQuery)
                if isAdmin:
                    if isAdmin[0] == 1:
                        _name = _form['name']
                        _address = _form['address']
                        _phoneNumber = _form['phoneNumber']
                        _concern = _form['concern']
                        _durationOfTreatment = _form['durationOfTreatment']
                        _startDateOfTreatment = _form['startDateOfTreatment']
                        _doctorInCharge = _form['doctorInCharge']
                        lastModified = datetime.datetime.now()
                        # startDateOfTreatment missing
                        if _name and _address and _phoneNumber and _concern and _durationOfTreatment and _doctorInCharge:
                            sqlQuery = f"UPDATE patient_details SET  patientName='{_name}',address='{_address}',phoneNumber='{_phoneNumber}',concern='{_concern}',durationOfTreatment='{_durationOfTreatment}',doctorInCharge='{_doctorInCharge}' WHERE authtoken='{_token}'"
                            sql_database(sqlQuery)
                            return {'status':'edited successfully'}
                        else:
                            return {'status':'false'}
                    else:
                        return {'status':'patient'}
                else:
                    return {'status':'null'}
            else:
                return {'status': 'token null'}
        except Exception as e:
            return internal_server_error
    elif request.method =='DELETE':
        try:
            _uid = request.json["uid"]
            _token = request.json["token"]
            if _uid and _token:
                sqlQuery = f"SELECT isAdmin FROM users WHERE uid='{_uid}' and '{_token}'"
                isAdmin = sql_database(sqlQuery)
                if isAdmin:
                    if isAdmin[0] == 1:
                        sqlQuery = f"DELETE patient_details, patient_records FROM patient_details INNER JOIN ON patieny_records ON patient_details.uid=patient_records.uid WHERE uid='{_uid}'"
                        sql_database(sqlQuery)
                        sqlQuery = f"DELETE from useres WHERE authtoken='{_token}'"
                        sql_database(sqlQuery)
                        return {'status':'deleted successfully'}
                    else:
                        return isAdmin[0]
                else:
                    return {'status':'null'}
            else:
                return {'status': 'token null'}
        except Exception as e:
            return internal_server_error
    else:
        return {'status': 'No Access'}
