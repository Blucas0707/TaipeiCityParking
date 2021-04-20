import json
import data_info
from sql import SQLDB
#convert tw97 to gs84
import twd97

class GET:
    def __init__(self):
        pass
        # self.data_url = data_info.data_url
        # self.data_name = data_info.data_name

    def collect_data(self):
        #read file
        with open("臺北市停車場資訊.json", "r") as f:
            # read file and convert to dict
            parking_lot_info_content = json.loads(f.read())

        with open("剩餘停車位數.json", "r") as f:
            # read file and convert to dict
            parking_live_content = json.loads(f.read())

        #parking lot info
        parking_lot_Updatetime = parking_lot_info_content["data"]["UPDATETIME"]
        parking_lot_data = parking_lot_info_content["data"]["park"]

        #parking live data
        parking_live_time = parking_live_content["data"]["UPDATETIME"]
        parking_live_data = parking_live_content["data"]["park"]

        #New dict
        Data_dict = {
            "data":{
                "INFO_UPDATETIME":"",
                "LIVE_UPDATETIME":"",
                "park":[]
            }
        }

        #save update time
        Data_dict["data"]["INFO_UPDATETIME"] = parking_lot_Updatetime
        Data_dict["data"]["LIVE_UPDATETIME"] = parking_live_time

        for data in parking_lot_data:
            #convert tw97 to gs84
            tw97x = float(data["tw97x"])
            tw97y = float(data["tw97y"])
            gs84 = twd97.towgs84(tw97x,tw97y)
            data["Xcord"] = gs84[0]
            data["Ycord"] = gs84[1]

            #delete tw97x, tw97y
            data.pop("tw97x")
            data.pop("tw97y")

            #combine live data with parking lot info
            dict = data
            id = data["id"]
            for live_data in parking_live_data:
                if live_data["id"] == id:
                    dict["availablecar"] = live_data["availablecar"]
                    dict["availablemotor"] = live_data["availablemotor"]
                    dict["availablebus"] = live_data["availablebus"]
                    break
            Data_dict["data"]["park"].append(dict)


        #save file in json format
        # open("TaipeiCtyParkingInfo.json", "w").write(json.dumps(Data_dict, ensure_ascii=False, indent = 4))
        # jsonformat = json.dumps(Data_dict, ensure_ascii=False,sort_keys=False, indent = 4)
        return Data_dict