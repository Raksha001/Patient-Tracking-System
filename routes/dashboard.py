from app import app, forbidden, internal_server_error
from db_config import mysql
from flask import jsonify, requeste

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

@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        _token = request.json["token"]
        if _token:
             sqlQuery = f"SELECT isAdmin FROM users WHERE uid='{_uid}' and '{_token}'"
                isAdmin = sql_database(sqlQuery)
                if isAdmin:
                    if isAdmin[0] == 1:
                        sqlQuery = f"SELECT count(uid) FROM patient_details"
                        patientCount = sql_database(sqlQuery)
                        sqlQuery = f"SELECT count(distinct(doctorInCharge)) FROM patient_details"
                        doctorCount = sql_database(sqlQuery)
                        sqlQuery = f"SELECT count(uid) FROM patient_details WHERE isCompleted=1"
                        completedCount = sql_database(sqlQuery)
                        sqlQuery = f"SELECT count(uid) FROM patient_details WHERE isCompleted=0"
                        liveCount = sql_database(sqlQuery)
                        return {'patientCount':patientCount,'doctorCount':doctorCount, 'completedCount':completedCount, 'liveCount':liveCount}
                    else:
                        return {'status':'Not admin'}
                else:
                    return {'status': 'null'}
        else:
            return {'status': 'null token'}
    except Exception as e:
        return internal_server_error
