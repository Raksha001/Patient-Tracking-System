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

@app.route('/simulation', methods=['GET'])
def simulation():
    try:
        """GET: To display files from doctors and patient"""
        if request.method == 'GET':
            _uid = request.form["uid"]
            _token = request.form["token"]

            if _token:
                _patientuid = request.form['patientuid']
                sqlQuery = f"SELECT isAdmin FROM users WHERE uid='{_uid}' and authtoken='{_token}'"
                isAdmin = sql_database(sqlQuery)
                print(isAdmin[0])
                if isAdmin:
                    if isAdmin["isAdmin"] == 1:
                        sqlQuery = f"SELECT imgUrl, uploadTime FROM patient_records WHERE uid='{_patientuid}' ORDER BY uploadTime asc"
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(sqlQuery)
                        patientRecords = cursor.fetchall()
                        conn.commit()
                        cursor.close()
                        conn.close()
                        sqlQuery = f"SELECT xray, designFile FROM patient_details WHERE uid='{_patientuid}'"
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(sqlQuery)
                        patientFiles = cursor.fetchall()
                        conn.commit()
                        cursor.close()
                        conn.close()
                        if len(patientFiles)>0 or len(patientRecords)>0:
                            return {'patientDetails':patientFiles, 'patientRecords':patientRecords}
                    else:
                        return {'status':'not admin'}
            else:
                return {'status':'null'}
        return {'status': 'null token'}
    except Exception as e:
        return internal_server_error()
