import mysql.connector
from mysql.connector import Error


def add(db,message):
    try:
        connection = mysql.connector.connect(
            user='root', 
            password='root',
            host='127.0.0.1',
            database='pubsub-issue')

        # 新增資料
        sql = "INSERT INTO "+db+"(msg, publishTime, subscribeTime, travelTime) VALUES ( %s, %s, %s, %s);"
        new_data = (message.data, message.publish_time, message.subscribe_time, (message.subscribe_time - message.publish_time).total_seconds())
        cursor = connection.cursor()
        cursor.execute(sql, new_data)

        # 確認資料有存入資料庫
        connection.commit()

    except Error as e:
        print("資料庫連接失敗：", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()