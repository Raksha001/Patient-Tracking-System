from app import app, forbidden, internal_server_error
from db_config import mysql
from flask import jsonify, request

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

@app.route('/patientprofile', methods=['GET'])
def patientprofile():
    try:
        _uid = request.form["uid"]
        _token = request.form["token"]
        if _token:
            sqlQuery = f"SELECT isAdmin FROM users WHERE authtoken='{_token}'"
            isAdmin = sql_database(sqlQuery)
            print(isAdmin)
            if isAdmin:
                if isAdmin[0] == 0:
                    sqlQuery = f"SELECT patientName,address,phoneNumber,concern,xray,designFile,durationOfTreatment, startDateOfTreatment,doctorInCharge, isCompleted FROM patient_details WHERE uid='{_uid}'"
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sqlQuery)
                    patientDetails = cursor.fetchall()
                    conn.commit()
                    cursor.close()
                    conn.close()
                    sqlQuery = f"SELECT imgUrl, uploadTime FROM patient_records WHERE uid='{_uid}' ORDER BY uploadTime asc"
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sqlQuery)
                    patientRecords = cursor.fetchall()
                    conn.commit()
                    cursor.close()
                    conn.close()
                    if len(patientDetails)>0 or len(patientRecords)>0:
                        return {'patientDetails':patientDetails, 'patientRecords':patientRecords}
                else:
                    return {'status':'Not Patient'}
            else:
                return {'status':'null'}
        return {'status': 'null token'}
    except Exception as e:
        return internal_server_error()