from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = "openclou_pattarai"
app.config['MYSQL_DATABASE_PASSWORD'] = "Pattarai@123"
app.config['MYSQL_DATABASE_DB'] = "openclou_next"
app.config['MYSQL_DATABASE_HOST'] = "opencloud.world"
mysql.init_app(app)