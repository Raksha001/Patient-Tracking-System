from app import app, forbidden
from db_config import mysql
from flask import jsonify, request, redirect

def generate_token(int userId):
    letters = string.ascii_letters + string.digits + string.punctuation
    jumble = ''.join(random.choice(letters) for i in range(22))
    sql_query = f"INSERT INTO users(authtoken) VALUES'{jumble}' WHERE userId='{userId}'"
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
            sqlQuery = f"SELECT uid, isAdmin from user where username='{_username}' and password='{_password}'"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            row = cursor.fetchone()
            conn.commit()
            if row:
                uid = row['uid']
                isAdmin = row['isAdmin']
            token = generate_token(uid)
            if isAdmin == 1:
                    return redirect("home.html")
            else:
                return redirect("patienthome.html")
            #res = jsonify(message)
            res.status_code = 200
            return res
        else:
            return forbidden()
    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()