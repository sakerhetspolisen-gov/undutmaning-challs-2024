import sqlite3
import os
import player

def prepareDB(p):
    # Prepare DB
    con = sqlite3.connect(p.myDbFileName)

    cur = con.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS anvandare (anvandarnamn TEXT PRIMARY KEY, losenord TEXT)")
    
    cur.execute("INSERT INTO anvandare VALUES ('harald','snuffe')")
    
    con.commit()
    con.close()

def checkPassword(p,user,pwd):

    con = sqlite3.connect(p.myDbFileName)

    cur = con.cursor()

    sqlstr = f'SELECT * FROM anvandare WHERE anvandarnamn=\'{user}\' AND losenord=\'{pwd}\''

    cur.execute(sqlstr)

    res = cur.fetchone()

    con.close()

    if res is None:
        return False
    
    return True

def checkUser(p,user):

    con = sqlite3.connect(p.myDbFileName)

    cur = con.cursor()

    sqlstr = f'SELECT * FROM anvandare WHERE anvandarnamn=\'{user}\''

    cur.execute(sqlstr)

    res = cur.fetchone()

    con.close()

    if res is None:
        return False
    
    return True
