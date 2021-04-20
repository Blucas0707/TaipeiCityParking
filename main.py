# import requests
# from bs4 import BeautifulSoup
# import gzip
# import json
from Download_file import Download
from get_data import GET
# from sql import SQLDB

#download data
file_download = Download().download()
GET().collect_data()
# #update parking lot info
# GET().SQL_parking_lot_info()
# #update parking live info
# GET().SQL_parking_live_info()















