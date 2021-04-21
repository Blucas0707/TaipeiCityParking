import pymysql
from dotenv import dotenv_values

#config
config = dotenv_values(".env")

class SQLDB:
    def __init__(self):
        self.host = config["SQL_HOST"]
        self.user = config["SQL_USER"]
        self.password = config["SQL_PASSWORD"]
        self.database = config["SQL_DATABASE"]
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)

    def close(self):
        self.conn.close()

    def update(self,sql = None, para =None):
        try :
            cursor = self.conn.cursor()
            cursor.execute(sql,para)
            self.conn.commit()
            # print("update success.")
            return True
        except:
            # print("update fail.")
            return False

    def read_available(self,keyword = None, area = None):

        if keyword == None:
            condition = ""
        else:
            condition = "where b.available"+ keyword + " > 0 and a.area like '%" + area + "%'"

        sql = "select a.*,b.availablecar,b.availablemotor,b.availablebus,b.update_time from taipei as a inner join taipei_live as b on a.id = b.id " + condition
        # print(sql)
        try :
            cursor = self.conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            data = {
                "total":-1,
                "live_update_time":"",
                "info_update_time": "",
                "park":[]
            }

            for result in results:
                park_data = {}
                park_data["id"] = result[0]
                park_data["area"] = result[1]
                park_data["name"] = result[2]
                park_data["room"] = result[3]
                park_data["summary"] = result[4]
                park_data["tel"] = result[5]
                park_data["latitude"] = result[6]
                park_data["longitude"] = result[7]
                park_data["payex"] = result[8]
                park_data["totalcar"] = result[9]
                park_data["totalmotor"] = result[10]
                park_data["totalcarbus"] = result[11]
                park_data["availablecar"] = result[13]
                park_data["availablemotor"] = result[14]
                park_data["availablebus"] = result[15]
                #save data into dict
                data["total"] = len(results)
                data["info_update_time"] = result[12]
                data["live_update_time"] = result[16]
                data["park"].append(park_data)
                # print(data["live_update_time"],result[16])
            return data
        except:
            data = {
                "error": True,
                "message": "Internal server error"
            }
            return data









