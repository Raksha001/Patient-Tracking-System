from app import app, forbidden, internal_server_error
from flask import jsonify, request, redirect, flash
from db_config import mysql
import os
from werkzeug.utils import secure_filename
import datetime
import random

UPLOAD_FOLDER = '/mnt/d/projects/Patient-Tracking-System/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg','PDF','PNG','JPG','JPEG'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
secretKey= os.urandom(24)
app.secret_key=secretKey

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

        # check if the post request has the file part
        if 'xray' not in request.files:
            resp = jsonify({'message' : 'No xray in the request'})
            resp.status_code = 400
            return resp

        _xray = request.files['xray']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if _xray.filename == '':
            return {'status':'No selected file'}
        if _xray and allowed_file(_xray.filename):
            filename = secure_filename(_xray.filename)
            xrayfile = _xray.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            xrayfilepath=os.path.join('/mnt/d/projects/Patient-Tracking-System/uploads', filename)

        # check if the post request has the file part
        if 'designFile' not in request.files:
            resp = jsonify({'message' : 'No design file in the request'})
            resp.status_code = 400
            return resp

        _designFile = request.files['designFile']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if _designFile.filename == '':
            return {'status':'No selected file'}
        if _designFile and allowed_file(_designFile.filename):
            filename = secure_filename(_designFile.filename)
            designfile = _designFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            designfilepath=os.path.join('/mnt/d/projects/Patient-Tracking-System/uploads', filename)
            print(designfilepath)

        username = _name
        randomnum = random.randrange(10,99)
        password = f'{username}@{randomnum}'
        _startDateOfTreatment = datetime.datetime.strptime(_startDateOfTreatment, '%Y-%m-%d')

        if _name and _address and _phoneNumber and _concern and _durationOfTreatment and _startDateOfTreatment and _doctorInCharge and _xray and _designFile:
            lastModified = datetime.datetime.now()
            sqlQuery = f"INSERT INTO users (username,password) VALUES ('{username}','{password}')"
            sql_database(sqlQuery)
            sqlQuery = f"SELECT uid FROM users WHERE username='{username}'"
            uid = sql_database(sqlQuery)
            print(uid[0])
            sqlQuery = f"INSERT INTO patient_details (uid, patientName, address, phoneNumber, concern, durationOfTreatment, startDateOfTreatment, doctorInCharge, xray, designFile, lastModified) VALUES ('{uid[0]}','{_name}', '{_address}', '{_phoneNumber}', '{_concern}', '{_durationOfTreatment}', '{_startDateOfTreatment}', '{_doctorInCharge}', '{xrayfilepath}', '{designfilepath}', '{lastModified}')"
            sql_database(sqlQuery)
            return {'status': 'success'}
        else:
            return {'status': 'false'}
    except Exception as e:
        return internal_server_error()

@app.route('/user', methods=['PUT','DELETE'])
def edituser():
    try:
        if request.method =='PUT':
            _uid = request.form["uid"]
            _token = request.form["token"]
            if _token:
                sqlQuery = f"SELECT isAdmin FROM users WHERE uid='{_uid}' and authtoken='{_token}'"
                isAdmin = sql_database(sqlQuery)
                print(isAdmin[0])
                if isAdmin:
                    if isAdmin[0] == 1:
                        _form = request.form
                        _patientuid = _form['patientuid']
                        _name = _form['name']
                        _address = _form['address']
                        _phoneNumber = _form['phoneNumber']
                        _concern = _form['concern']
                        _durationOfTreatment = _form['durationOfTreatment']
                        _startDateOfTreatment = _form['startDateOfTreatment']
                        _doctorInCharge = _form['doctorInCharge']
                        _startDateOfTreatment = datetime.datetime.strptime(_startDateOfTreatment, '%Y-%m-%d')
                        lastModified = datetime.datetime.now()
                        
                        # startDateOfTreatment missing
                        if _name and _address and _phoneNumber and _concern and _durationOfTreatment and _startDateOfTreatment and _doctorInCharge:
                            sqlQuery = f"UPDATE patient_details SET  patientName='{_name}',address='{_address}',phoneNumber='{_phoneNumber}',concern='{_concern}',durationOfTreatment='{_durationOfTreatment}',startDateOfTreatment='{_startDateOfTreatment}',doctorInCharge='{_doctorInCharge}' WHERE uid='{_patientuid}'"
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

        elif request.method =='DELETE':
            _uid = request.form["uid"]
            _token = request.form["token"]
            if _uid and _token:
                sqlQuery = f"SELECT isAdmin FROM users WHERE uid='{_uid}' and authtoken='{_token}'"
                isAdmin = sql_database(sqlQuery)
                if isAdmin:
                    if isAdmin[0] == 1:
                        _patientuid = request.form['patientuid']
                        sqlQuery = f"DELETE patient_details, patient_records FROM patient_details INNER JOIN ON patient_records ON patient_details.uid=patient_records.uid WHERE patient_details.uid='{_patientuid}'"
                        sql_database(sqlQuery)
                        sqlQuery = f"DELETE from users WHERE uid='{_patientuid}'"
                        sql_database(sqlQuery)
                        return {'status':'deleted successfully'}
                    else:
                        return isAdmin[0]
                else:
                    return {'status':'null'}
            else:
                return {'status': 'token null'}
        else:
            return {'status': 'No Access'}
    except Exception as e:
        return internal_server_error()
