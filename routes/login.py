from app import app, forbidden
from db_config import mysql
from flask import jsonify, request, redirect

def generate_token(userId):
    letters = string.ascii_letters + string.digits + string.punctuation
    jumble = ''.join(random.choice(letters) for i in range(22))
    sql_query = f"INSERT INTO users(authtoken) VALUES('{jumble}') WHERE userId='{userId}'"
    authoken = cursor.execute(sqlQuery)
    conn.commit()
    return jumble

@app.route('/login', methods=['POST'])
def login():
    try:
        _form = request.form
        _username = _form['username']
        _password = _form['password']

        if _name and _password and request.method == 'POST':
            # insert record in database
            sqlQuery = f"SELECT uid, isAdmin from users where username='{_username}' and password='{_password}'"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            row = cursor.fetchall()
            conn.commit()
            if row:
                uid = row['uid']
                isAdmin = row['isAdmin']
                authtoken = generate_token(uid)
                cursor.close()
                conn.close()
                if isAdmin == 1:
                    return {'status':'true','token': authtoken}
                else:
                    return {'status' : 'false'}
            status_code = 200
        else:
            return forbidden()
    except Exception as e:
        return internal_server_error()
        

@app.route('/logout', methods['POST'])
def logout():
    try:
        _token = request.json["token"]
        if _token and request.method == 'POST':
            sqlQuery = f"Delete authtoken from users where authtoken='{token}'"
            return {'status':'true'}
        else:
            return forbidden()
    except Exception as e:
        return internal_server_error()