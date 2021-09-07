from app import app, forbidden, internal_server_error
from flask import jsonify, request, redirect, flash
from db_config import mysql
import os
from werkzeug.utils import secure_filename
import datetime
import random

UPLOAD_FOLDER = '/mnt/d/projects/Patient-Tracking-System/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','PNG','JPG','JPEG'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
secretKey= os.urandom(24)
app.secret_key=secretKey

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        ''' POST: Register user details '''
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
            xrayfilepath=os.path.join('uploads', filename)

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
            designfilepath=os.path.join('uploads', filename)
            print(designfilepath)

        #create username and password for patient
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
            print(uid["uid"])
            sqlQuery = f"INSERT INTO patient_details (uid, patientName, address, phoneNumber, concern, durationOfTreatment, startDateOfTreatment, doctorInCharge, xray, designFile, lastModified) VALUES ('{uid["uid"]}','{_name}', '{_address}', '{_phoneNumber}', '{_concern}', '{_durationOfTreatment}', '{_startDateOfTreatment}', '{_doctorInCharge}', '{xrayfilepath}', '{designfilepath}', '{lastModified}')"
            sql_database(sqlQuery)
            return {'status': 'success'}
        else:
            return {'status': 'false'}
    except Exception as e:
        return internal_server_error()

@app.route('/user', methods=['GET','PUT','DELETE'])
def edituser():
    try:
        """ 
        GET: Display user details for edit
        PUT: Edit User 
        DELETE: Deletes User
        """
        if request.method == 'GET':
            _uid = request.form["uid"]
            _token = request.form["token"]

            if _token:
                sqlQuery = f"SELECT isAdmin FROM users WHERE uid='{_uid}' and authtoken='{_token}'"
                isAdmin = sql_database(sqlQuery)
                print(isAdmin["isAdmin"])
                if isAdmin:
                    if isAdmin["isAdmin"] == 1:
                        #get details to display
                        _patientuid = request.form['patientuid']
                        sqlQuery = f"SELECT patientName,address,phoneNumber,concern,xray,designFile,durationOfTreatment, startDateOfTreatment,doctorInCharge, isCompleted FROM patient_details WHERE uid='{_patientuid}'"
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(sqlQuery)
                        row = cursor.fetchall()
                        conn.commit()
                        cursor.close()
                        conn.close()

                        if row:
                            return {'userdetails':row}
                    else:
                        return {'status':'Not Admin'}
                else:
                    return {'status': 'null'}
            else:
                return {'status': 'null token'}

        elif request.method =='PUT':
            _uid = request.form["uid"]
            _token = request.form["token"]
            if _token:
                sqlQuery = f"SELECT isAdmin FROM users WHERE uid='{_uid}' and authtoken='{_token}'"
                isAdmin = sql_database(sqlQuery)
                print(isAdmin["isAdmin"])
                if isAdmin:
                    if isAdmin["isAdmin"] == 1:
                        #update entries
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
                    if isAdmin["isAdmin"] == 1:
                        _patientuid = request.form['patientuid']
                        #to delete user details from patient_details, patient_records and users table
                        sqlQuery = f"DELETE from patient_details WHERE uid='{_patientuid}'"
                        sql_database(sqlQuery)
                        sqlQuery = f"DELETE from patient_records WHERE uid='{_patientuid}'"
                        sql_database(sqlQuery)
                        sqlQuery = f"DELETE from users WHERE uid='{_patientuid}'"
                        sql_database(sqlQuery)
                        return {'status':'deleted successfully'}
                    else:
                        return isAdmin["isAdmin"]
                else:
                    return {'status':'null'}
            else:
                return {'status': 'token null'}
        else:
            return {'status': 'No Access'}
    except Exception as e:
        return internal_server_error()
