import sqlite3
  
try:
    
    # Connect to DB and create a cursor
    sqliteConnection = sqlite3.connect('sql.db')
    cursor = sqliteConnection.cursor()

    # cursor object
    cursor_obj = sqliteConnection.cursor()
 
    # Drop the tables if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS POSTS")
    cursor_obj.execute("DROP TABLE IF EXISTS USERS")
    cursor_obj.execute("DROP TABLE IF EXISTS FLAGS")
 
    # Creating table POSTS
    table = """ CREATE TABLE POSTS (
                User_Name char(25) NOT NULL,
                Content VARCHAR(1000) NOT NULL,
                Post_id INT NOT NULL
            ); """
 
    cursor_obj.execute(table)

    # Creating table USERS
    table = """ CREATE TABLE USERS (
                User_ID INT NOT NULL,
                User_Name varchar(512) NOT NULL,
                User_Password varchar(50) NOT NULL
            ); """
 
    cursor_obj.execute(table)

    # Creating table FLAGS
    table = """ CREATE TABLE FLAGS (
                Flag char(50) NOT NULL
            ); """
 
    cursor_obj.execute(table)
    #Load flag
    cursor.execute('''INSERT INTO FLAGS VALUES ('undut{grattis-till-flaggan}')''')

    # Load users
    cursor.execute('''INSERT INTO USERS VALUES (1, 'bob runsköld','password')''')
    cursor.execute('''INSERT INTO USERS VALUES (2, 'alice yxa','password1')''')
    cursor.execute('''INSERT INTO USERS VALUES (3, 'edda flint','password2')''')
    cursor.execute('''INSERT INTO USERS VALUES (4, 'harald blåtand','password3')''')
    # load basic posts
    cursor.execute('''INSERT INTO POSTS VALUES ('bob runsköld','jag har låtit resa denna blogg för att inte glömma harald blåtands hemska protokoll',1)''')
    cursor.execute('''INSERT INTO POSTS VALUES ('bob runsköld','länge leve 802.11ax!',2)''')
    cursor.execute('''INSERT INTO POSTS VALUES ('alice yxa','Vilken fantastisk blogg det här är! jag hoppas ingen försöker göra något konstigt med den!',3)''')
    cursor.execute('''INSERT INTO POSTS VALUES ('edda flint','Jag håller med dig alice!',4)''')
    cursor.execute('''INSERT INTO POSTS VALUES ('bob runsköld','Tack alice och edda!',5)''')
    cursor.execute('''INSERT INTO POSTS VALUES ('harald blåtand','hahaha jag har all makt trots att mitt namn är harald blåtand och inte tengil! ingen direktverkan här inte...',6)''')

    print("Table is Ready")

    print("Data Inserted in the table USERS: ")
    data=cursor.execute('''SELECT * FROM USERS''')
    for row in data:
        print(row)

    # Close the cursor
    cursor.close()

    cursor = sqliteConnection.cursor()
    print("Data Inserted in the table POSTS: ")
    data=cursor.execute('''SELECT * FROM POSTS''')
    for row in data:
        print(row)

    # Close the cursor
    cursor.close()

    cursor = sqliteConnection.cursor()
    print("Data Inserted in the table FLAGS: ")
    data=cursor.execute('''SELECT * FROM FLAGS''')
    for row in data:
        print(row)

    # Close the cursor
    cursor.close()

    sqliteConnection.commit()
  
# Handle errors
except sqlite3.Error as error:
    print('Error occured - ', error)
  
# Close DB Connection irrespective of success
# or failure
finally:
    
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed')
