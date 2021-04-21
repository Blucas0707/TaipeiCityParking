import json
import data_info
from sql import SQLDB
#convert tw97 to gs84
import twd97

#SQL
mysql = SQLDB()

class GET:
    def __init__(self):
        pass
        # self.data_url = data_info.data_url
        # self.data_name = data_info.data_name

    def collect_data(self):
        #read file parking lot information
        with open("臺北市停車場資訊.json", "r") as f:
            # read file and convert to dict
            parking_lot_info_content = json.loads(f.read())

        # parking lot info
        parking_lot_Updatetime = parking_lot_info_content["data"]["UPDATETIME"]
        parking_lot_data = parking_lot_info_content["data"]["park"]

        # get data and save to sql
        for data in parking_lot_data:
            para = []

            #轉換停車場twd97 座標成gs84 經緯度
            tw97x = float(data["tw97x"])
            tw97y = float(data["tw97y"])
            gs84 = twd97.towgs84(tw97x,tw97y)

            #put data into para for sql
            para.append(data["id"]) #id
            para.append(data["area"]) #area
            para.append(data["name"]) #name
            para.append(1) #room
            para.append(data["summary"]) #summary
            para.append(data["tel"]) #tel
            para.append(gs84[0]) #latitude
            para.append(gs84[1]) #longitude
            para.append(data["payex"]) #payex
            para.append(data["totalcar"]) #totalcar
            para.append(data["totalmotor"]) #totalmotor
            para.append(data["totalbus"]) #totalbus
            para.append(parking_lot_Updatetime) #update_time
            para = tuple(para)
            #save into sql
            sql = "replace into taipei (id, area, name, room, summary, tel, latitude, longitude, payex, totalcar, totalmotor, totalbus, update_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mysql.update(sql,para)

        #read file, parking live data
        with open("剩餘停車位數.json", "r") as f:
            # read file and convert to dict
            parking_live_content = json.loads(f.read())

        #parking live data
        parking_live_time = parking_live_content["data"]["UPDATETIME"]
        parking_live_data = parking_live_content["data"]["park"]

        #get data and save to sql
        for data in parking_live_data:
            para = []

            # put data into para for sql
            para.append(data["id"])  # id
            para.append(data["availablecar"]) #availablecar
            para.append(data["availablemotor"])  # availablemotor
            para.append(data["availablebus"])  # availablebus
            para.append(parking_live_time)  # update_time
            # save into sql
            sql = "replace into taipei_live (id, availablecar, availablemotor, availablebus, update_time) values (%s,%s,%s,%s,%s)"
            mysql.update(sql, para)

