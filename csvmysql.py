import pymysql
import csv

db = pymysql.connect(
    host='localhost',
    user='root',
    password="root",
    db='phonepedb',
)


cursor = db.cursor()
csv_data = csv.reader(open('data/Longitude_Latitude_State_Table.csv'))
next(csv_data)
for row in csv_data:
    cursor.execute('INSERT INTO longitude_latitude_state_table(code,Latitude,Longitude,state) VALUES(%s, %s, %s, %s)',row)

db.commit()
cursor.close()