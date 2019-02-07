import os
import string
import sqlite3


database = 'spoilerbot.db'

def doDb():
    if os.path.isfile(database):
        print("DB found, yeet.")
    else:
        print("Creatin' the DB!")
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('''CREATE TABLE channel
                     (serverid text, channelid text)''')
        c.execute('''CREATE TABLE whitelist
                     (serverid text, userid text)''')
        c.execute('''CREATE TABLE gamestatus
                     (serverid text, status text)''')
        c.execute('''CREATE TABLE gameanswer
                     (serverid text, answer text)''')     
        conn.commit()
        conn.close()
        print("Bazinga, its done.")

def gameStatus(mode, value, sid):
    output = "No spoiler game is currently being held :("
    conn = sqlite3.connect(database)
    c = conn.cursor()
    if (mode == "get"):
        c.execute('SELECT status FROM gamestatus WHERE serverid = (?)', (sid,))
        q = c.fetchall()
        for row in q:
            crow = str(row).replace("(","").replace(")","").replace(",","").replace("'","")
            if (crow == "0"):
                output = "No spoiler game is currently being held :("
            if (crow == "1"):
                output = "There is a spoiler game being currently held!"   
    if (mode == "set"):
        c.execute('SELECT status FROM gamestatus WHERE serverid = (?)', (sid,))
        q = c.fetchall()
        if len(q)==0:
            c.execute("Insert into gamestatus (serverid, status) values (?,?)", (sid, value))
            print(sid)
            output = "Added and status!!"
        c.execute('UPDATE gamestatus SET status=? WHERE serverid=?', [value, sid])
        conn.commit()
        conn.close()      
        output = "Updated status!"
    return output


def whiteList(mode, id, sid):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    if (mode == "add"):
        c.execute('SELECT userid FROM whitelist WHERE serverid = (?)', (sid,))
        q = c.fetchall()
        for row in q:
            if id in row:
                return("User is already whitelisted.")
        c.execute("insert into whitelist (serverid, userid) values (?,?)", (sid, id))
        conn.commit()
        conn.close()
        return("Whitelisted user.")
    if (mode == "del"):
        c.execute('DELETE FROM whitelist WHERE (user=(?) AND serverid=(?))', (id, sid))
        conn.commit()
        conn.close()
        return "Removed user from whitelist."
