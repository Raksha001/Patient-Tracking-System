from app import app, forbidden, internal_server_error
from db_config import mysql
from flask import jsonify, request
import traceback


def sql_database(sql_query):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        row = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return row
    except Exception as e:
        print(e)

def sql_database2(sql_query):
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

@app.route('/patientprofile', methods=['GET'])
def patientprofile():
    try:
        
        multi_dict = request.args
        for key in multi_dict:
            print(multi_dict.get(key))
            print(multi_dict.getlist(key))
        _uid = request.args["uid"]
        _token = request.args["token"]
        if _token:
            sqlQuery = f"SELECT isAdmin FROM users WHERE authtoken='{_token}'"
            traceback.print_exc()
            isAdmin = sql_database2(sqlQuery)
            print(isAdmin["isAdmin"])
            if isAdmin:
                if isAdmin["isAdmin"] == 0:
                    sqlQuery = f"SELECT patientName,address,phoneNumber,concern,xray,designFile,durationOfTreatment, startDateOfTreatment,doctorInCharge, isCompleted FROM patient_details WHERE uid='{_uid}'"
                    patientDetails = sql_database(sqlQuery)
                    sqlQuery = f"SELECT imgUrl, uploadTime FROM patient_records WHERE uid='{_uid}' ORDER BY uploadTime asc"
                    patientRecords = sql_database(sqlQuery)
                    if len(patientDetails)>0 or len(patientRecords)>0:
                        return {'patientDetails':patientDetails, 'patientRecords':patientRecords}
                else:
                    return {'status':'Not Patient'}
            else:
                return {'status':'null'}
        return {'status': 'null token'}
    except Exception as e:
        return internal_server_error()