from mysql_connector import conn

class JobSql(object):
    def add(data):
        sql = conn.cursor()

        # TODO 這邊寫插入資料的SQL語法

        conn.commit()
