import sqlite3
import json


con = sqlite3.connect("mybd.sqlite",check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

def videosall(Item_id):

    q="SELECT * FROM video WHERE Item_id=?"
    data= cur.execute(q,(Item_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json



def x(Item_id,video_id):
    q="SELECT * FROM video WHERE Item_id=? and video_id=?"
    data= cur.execute(q,(Item_id,video_id)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

print(x(1,1))
