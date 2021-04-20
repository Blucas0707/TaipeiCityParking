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

    def SAVE_PARKING_LOT_INFO(self, para= None):
        #judge if data exist
        sql = "select count(*) from parking_lot_info where parking_lot_id = %s"
        parking_lot_id = para[0]
        # print(parking_lot_id,type(parking_lot_id))
        cursor = self.conn.cursor()
        cursor.execute(sql, parking_lot_id)
        result = cursor.fetchone()
        # print(result)
        if result[0] == 0:
            #insert data into sql
            sql = "INSERT INTO parking_lot_info (parking_lot_id, area, name, summary, address, tel, payex, tw97x, tw97y, totalcar, totalmotor, totalbus) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, para)
            self.conn.commit()
            return True
        else:
            return False

    def UPDATE_PARKING_LIVE_INFO(self, para=None):
        sql = "select count(*) from parking_live_info where parking_live_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(sql, para[0])
        result = cursor.fetchone()[0]
        if result == 1:
            sql = "update parking_live_info set availablecar = %s, availablemotor = %s, availablebus = %s where parking_live_id = %s"
            para = (para[1],para[2],para[3],para[0])
            cursor.execute(sql, para)
            self.conn.commit()
        else:
            sql = "insert into parking_live_info (parking_live_id,availablecar,availablemotor,availablebus) values (%s,%s,%s,%s)"
            cursor.execute(sql, para)
            self.conn.commit()

    def UPDATE_TIME(self, para = None):
        sql = "update update_time set update_time = %s where name = %s"
        cursor = self.conn.cursor()
        cursor.execute(sql,para)
        self.conn.commit()





