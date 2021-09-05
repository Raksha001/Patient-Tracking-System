from app import app, forbidden
from db_config import mysql
from flask import jsonify, request, redirect
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
datetime_fmt = '%Y-%m-%d %H:%M:%S

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
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

@app.route('/register',methods['POST'])
def register():
    try:
        _form = request.form
        _name = _form['name']
        _address = _form['address']
        _phoneNumber = _form['phoneNumber']
        _concern = _form['concern']
        _durationOfTreatment = _form['durationOfTreatment']
        _startDateOfTreatmemt = _form['startDateOfTreatmemt']
        _doctorInCharge = _form['doctorInCharge']
        xray = upload_file()
        design = upload_file()
        if _name and _address and _phoneNumber and _concern and _durationOfTreatment and _startDateOfTreatmemt and _doctorInCharge and xray and design:
            # Convert time range to UTC tz datetime var
            lastModified = datetime.strptime(str(_startTime), datetime_fmt).replace(tzinfo=pytz.UTC)
            sqlQuery = f"INSERT INTO patientDetails (patientName, address, phoneNumber, concern, durationOfTreatment, startDateOfTreatmemt, doctorInCharge, xray, designFile, lastModified) VALUES ('{_name}', '{_address}', '{_phoneNumber}', '{_concern}', '{_durationOfTreatment}', '{_startDateOfTreatmemt}', '{_doctorInCharge}', '{_xray}', '{_designFile}', '{lastModified}')"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            conn.commit()
            cursor.close()
            conn.close()
            return {'status': 'success'}
        else:
            return {'status': 'false'}
    except Exception as e:
        return internal_server_error()

        