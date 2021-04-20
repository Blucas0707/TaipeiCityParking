from Download_file import Download
from get_data import GET
import json
from flask import *

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# Pages
@app.route("/")
def index():
	return render_template("index.html")

#API
@app.route("/api")
def api():
    #download file
    file_download = Download().download()
    #collect data & save as json format
    jsonformat = json.dumps(GET().collect_data(),ensure_ascii = False, sort_keys= False, indent=4)
    return jsonformat


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

app.run(host = "0.0.0.0", port =3000)