from app import app, forbidden, internal_server_error
from db_config import mysql
from flask import jsonify, request, redirect
import string, random

def generate_token():
    letters = string.ascii_letters + string.digits
    jumble = ''.join(random.choice(letters) for i in range(22))
    return jumble

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


@app.route('/login', methods=['POST'])
def login():
    try:
        _form = request.form
        _username = _form['username']
        _password = _form['password']

        if _username and _password and request.method == 'POST':
            # insert record in database
            sqlQuery = f"SELECT uid, isAdmin from users where username='{_username}' and password='{_password}'"
            uid, isAdmin = sql_database(sqlQuery)
           
            if uid:
                authtoken = generate_token()
                sql_query = f"UPDATE users SET authtoken='{authtoken}' WHERE uid='{uid}'"
                sql_database(sql_query)
                
                if isAdmin == 1:
                    return {'status':'admin','token': authtoken, 'uid':uid}
                else:
                    return {'status' : 'patient', 'token': authtoken, 'uid':uid}
                status_code = 200
            else:
                return {'status':'false'}
            
        else:
            return forbidden()
    except Exception as e:
        return internal_server_error()
        

@app.route('/logout', methods=['POST'])
def logout():
    try:
        _token = request.form["token"]
        print(_token)
        if _token: 
            sqlQuery = f"Update users set authtoken=null where authtoken='{_token}'"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            conn.commit()
            cursor.close()
            conn.close()
            return {'status':'true'}
        else:
            return forbidden()
    except Exception as e:
        return internal_server_error()