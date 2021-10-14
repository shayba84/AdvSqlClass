from tkinter import *
from typing import Union, Any


import mysql.connector
from mysql.connector.cursor import CursorBase, MySQLCursor, MySQLCursorBuffered, MySQLCursorRaw, \
    MySQLCursorBufferedRaw, \
    MySQLCursorDict, MySQLCursorBufferedDict, MySQLCursorNamedTuple, MySQLCursorBufferedNamedTuple, MySQLCursorPrepared

#from mysql.connector.cursor_cext import CMySQLCursor
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", database="playgroud"
)

def Get_CityList():
    cursor = mydb.cursor()
    cursor.callproc('sp_get_citys_list', args=())
    dataout=[]
    for result in cursor.stored_results():
        res=result.fetchall()
        for data in res:
            dataout.append(data[0])


    return dataout

def Get_streetList():
    cursor = mydb.cursor()
    cursor.callproc('sp_get_street_list', args=())
    dataout=[]
    for result in cursor.stored_results():
        res=result.fetchall()
        for data in res:
            dataout.append(data[0])


    return dataout




print(mydb)

mycursor: Union[Union[
                    CursorBase, MySQLCursor, MySQLCursorBuffered, MySQLCursorRaw, MySQLCursorBufferedRaw,
                    MySQLCursorDict, MySQLCursorBufferedDict, MySQLCursorNamedTuple, MySQLCursorBufferedNamedTuple,
                    MySQLCursorPrepared], Any] = mydb.cursor()

mycursor.execute("select city.city, city.street, equipment.sports_equipment "
                 "from city "
                 "inner join city_ground_id  on city.city_id = city_ground_id.ID_city "
                 "inner join equipment on city_ground_id.Equipment_ID = equipment.idequipment_id")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)

window = Tk()
window.geometry('1200x500')
window.title("Welcome to payground's order app")
logo = PhotoImage(file="img.png")
w1 = Label(window, compound=CENTER, image=logo)#.pack(side="right")
w1.place(x=0, y=0)

cityresult=Get_CityList()
streetresult=Get_streetList()


lbl_playgame = Label(window, text="enter play game")
lbl_playgame.grid(column=0, row=0)

txt_playname = Entry(window, width=10)
txt_playname.grid(column=1, row=0)


def get_play_name():
    assert isinstance(mycursor, object)
    mycursor.execute("select city.city, city.street,equipment.sports_equipment from city inner join city_ground_id  on city.city_id = city_ground_id.ID_city inner join equipment on city_ground_id.Equipment_ID = equipment.idequipment_id where sports_equipment  = %s ", [txt_playname.get()])
    result = mycursor.fetchall()
    if result is None:
        lbl_playgame.configure(text=txt_playname.get())

    else:
        lbl_playgame.configure(text=result)


btn = Button(window, text="get place", command=get_play_name)
btn.grid(column=3, row=0)

lbl_playgameconfigure = Label()
lbl_playgameconfigure.grid(column=2, row=0)
# -----------------------------------------------------------------------------------------------------------------
lbl_cityname = Label(window, text="enter city name")
lbl_cityname.grid(column=0, row=1)

txt_street_name = Entry(window, width=10)
txt_street_name.grid(column=1, row=1)


def get_street_name(lbl_street_name=None):
    assert isinstance(mycursor, object)
    mycursor.execute("select street from city where city = %s", [txt_street_name.get()])
    result = mycursor.fetchall()
    if result is None:
        lbl_street_name.configure(text=txt_street_name.get())

    else:
        lbl_cityname.configure(text=result)


btn = Button(window, text="get street", command=get_street_name)
btn.grid(column=3, row=1)

lbl_cityname = Label()
lbl_cityname.grid(column=2, row=1)

# --------------------------------------------------------------------------------------------------------
lbl_timegame1 = Label(window, text="enter game for show times")
lbl_timegame1.grid(column=0, row=2)

txt_timegame1 = Entry(window, width=10)
txt_timegame1.grid(column=1, row=2)


def get_time_game():
    assert isinstance(mycursor, object)
    mycursor.execute("select date,start_time,end_time,type,city,street from playgroud.time_orderd inner join city_ground_id on city_ground_ID = ID_city inner join playground on ID_Playground = playground_id inner join city on ID_city = city_id where type = %s", [txt_timegame1.get()])
    result = mycursor.fetchone()
    if result is None:
        lbl_timegame1.configure(text=txt_timegame1.get())

    else:
        lbl_timegame1.configure(text=result)


btn = Button(window, text="get Schedule", command=get_time_game)
btn.grid(column=3, row=2)

lbl_timegame1 = Label()
lbl_timegame1.grid(column=2, row=2)

USER = [
"haim",
"moshe",
"itzik",
"dana",
"yuval"]
def order_playground():
    cursor = mydb.cursor()
    args = (txt_odate.get(), txt_odateStart.get(), txt_odateEnd.get(), variable.get(), vstreet.get(), 'football',vuser.get())
    cursor.callproc('SP_insertOrder', args)


lbl_ccity = Label(window, text="choose city")
lbl_ccity.grid(column=0, row=3)

variable = StringVar(window)
variable.set(cityresult[0]) # default value

w = OptionMenu(window, variable, *cityresult)
w.grid(column=1, row=3)

lbl_cstreet = Label(window, text="choose street")
lbl_cstreet.grid(column=2, row=3)

vstreet = StringVar(window)
vstreet.set(streetresult[0]) # default value

ddstreet = OptionMenu(window, vstreet, *streetresult)
ddstreet.grid(column=3, row=3)

lbl_cuser = Label(window, text="choose user")
lbl_cuser.grid(column=4, row=3)

vuser = StringVar(window)
vuser.set(USER[0]) # default value

dduser = OptionMenu(window, vuser, *USER)
dduser.grid(column=5, row=3)

lbl_odate = Label(window, text="date 2021-02-20")
lbl_odate.grid(column=6, row=3)

txt_odate = Entry(window, width=10)
txt_odate.grid(column=7, row=3)

lbl_odateStart = Label(window, text="start time 08:00:00")
lbl_odateStart.grid(column=8, row=3)

txt_odateStart = Entry(window, width=10)
txt_odateStart.grid(column=9, row=3)


lbl_odateEnd = Label(window, text="end time 08:00:00")
lbl_odateEnd.grid(column=10, row=3)

txt_odateEnd = Entry(window, width=10)
txt_odateEnd.grid(column=11, row=3)

btnorder = Button(window, text="order", command=order_playground)
btnorder.grid(column=11, row=3)

window.mainloop()