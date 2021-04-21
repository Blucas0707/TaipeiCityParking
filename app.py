from Download_file import Download
from get_data import GET
import json
from flask import *
from sql import SQLDB

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

def update_raw():
	#download&update to sql file
	Download().download()
	GET().collect_data()


# Pages
@app.route("/")
def index():
	return render_template("index.html")

#API
@app.route("/api/available", methods = ["GET"])
def api():
	#get keyword, area
	keyword = request.args.get("keyword")
	area = request.args.get("area") if request.args.get("area")!=None else ""

	#get keyword
	if keyword in ["car","motor","bus"] or keyword == None:
		#update raw data
		update_raw()
		# sql
		mysql = SQLDB()
		#get data from sql
		data = mysql.read_available(keyword,area)
		#close sql
		mysql = SQLDB().close()

		#judge empty date
		if data["total"] == -1:
			data = {
				"error": True,
				"message": "No data."
			}
		#convert into json format
		jsonformat = json.dumps(data, sort_keys=False, indent =4)
		return jsonformat
	else:
		data = {
			"error": True,
			"message": "keyword not equals to car, motor or bus."
		}
		return json.dumps(data_dict, sort_keys=False, indent=4)

#Error handle
@app.errorhandler(500)
def internal_error(error):
	data_dict = {
		"error": True,
  		"message": "Internal Server Error."
	}
	return json.dumps(data_dict, sort_keys= False, indent= 4)

@app.errorhandler(404)
def not_found_error(error):
	data_dict = {
		"error": True,
  		"message": "Website not found."
	}
	return json.dumps(data_dict, sort_keys= False, indent= 4)

@app.errorhandler(403)
def not_found_error(error):
	data_dict = {
		"error": True,
  		"message": "Forbidden. Access denied."
	}
	return json.dumps(data_dict, sort_keys= False, indent= 4)

# app.run(host = "0.0.0.0", port =3000)
app.run(host = "0.0.0.0", port =3000, ssl_context ='adhoc') #https: 隨機生成SSL簽證
# app.run(host = "0.0.0.0", port =3000,  ssl_context=('cert.pem', 'key.pem')) #生成自己的SSL 簽證
