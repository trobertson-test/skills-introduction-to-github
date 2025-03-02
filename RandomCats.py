import requests
import json
import sqlite3
from PIL import Image
import os
import datetime

dt = datetime.datetime.now()
year,week_num,day_of_week = dt.isocalendar()

def db_setup():
    conn = sqlite3.connect('db.sqlite3')
    conn.execute('''CREATE TABLE CATS
         (ID            TEXT      PRIMARY KEY   NOT NULL,
         YEAR           INTEGER                 NOT NULL,
         WEEK           INTEGER                 NOT NULL,
         DAY            INTEGER                 NOT NULL,
         IMAGE          TEXT                    NOT NULL);
         ''')
    conn.close()
    
def get_image(i):
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    d = str(response.json())[1:-1].replace("'", '"')
    response = json.loads(d)
    id = str(response["id"])
    response2 = requests.get(response['url'])
    image_name = id + ".jpg"
    file_name = "C:\\Users\\trobertson\\Desktop\\projects\\TheCatApi\\thecat_django\\config\\randomcats\static\\" + image_name
    f = open(file_name, "wb")
    p = response2._content
    f.write(p)
    f.close()

    connection_obj = sqlite3.connect('db.sqlite3') 
    cursor_obj = connection_obj.cursor() 
    statement = '''SELECT * FROM randomcats_day order by id desc'''
    cursor_obj.execute(statement) 
    output = cursor_obj.fetchone() 
    day_id = output[0]
    connection_obj.close()
    
    connection_obj = sqlite3.connect('db.sqlite3') 
    cursor_obj = connection_obj.cursor() 
    statement = '''SELECT * FROM randomcats_cat order by id desc'''
    cursor_obj.execute(statement) 
    output = cursor_obj.fetchone()
    cursor_obj.close()
    id = output[0] + 1
    
    cat = "test cat"
    votes = 0
    conn = sqlite3.connect('db.sqlite3')
    print("INSERT INTO randomcats_cat (id, cat, votes, day_id, image_name) VALUES(?, ?, ?, ?, ?)",(id, cat, votes, day_id, image_name))
    conn.execute("INSERT INTO randomcats_cat (id, cat, votes, day_id, image_name) VALUES(?, ?, ?, ?, ?)",(id, cat, votes, day_id, image_name))
    conn.commit()
    conn.close()
    #im.show()
    
def set_date():
    dt = datetime.datetime.now()
    year,week_num,day_of_week = dt.isocalendar()
    connection_obj = sqlite3.connect('db.sqlite3') 
    cursor_obj = connection_obj.cursor() 
    statement = '''SELECT * FROM randomcats_day order by id desc'''
    cursor_obj.execute(statement) 
    output = cursor_obj.fetchone() 
    id = output[0] + 1
    connection_obj.close()
    conn = sqlite3.connect('db.sqlite3')
    conn.execute("INSERT INTO randomcats_day (ID, YEAR, WEEK, DAY) VALUES(?, ?, ?, ?)",(id, year, week_num, day_of_week))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    path = './db.sqlite3'
    #if os.path.isfile(path):
    #    print('DB Found')
    #else:
    #    print('Creating DB')
    #    db_setup()
    i = 0
    set_date()
    while i < 6:
        get_image(i)
        i +=1