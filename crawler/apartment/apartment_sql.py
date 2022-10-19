from mysql_connector import conn

class ApartmentSql(object):
    def add(data):
        sql = conn.cursor()

        # TODO 這邊寫插入資料的SQL語法

        conn.commit()
