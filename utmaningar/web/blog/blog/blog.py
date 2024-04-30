#from curses.ascii import US
from os import replace
from flask import Flask, request, redirect
import json
import sqlite3
import html

isLogedIn = False
id = 0
glob_error = ''


def logintoblog(username, password):
    id = 0
    sqliteConnection = sqlite3.connect('sql.db')
    global glob_error
    glob_error = ''

    try:
        
        # Connect to DB and create a cursor
        
        cursor = sqliteConnection.cursor()
    
        sql = """SELECT User_ID 
                    from USERS 
                    where User_Password = ? 
                    AND User_name = ?"""
        args = (password,username)
        cursor = cursor.execute(sql, args)
    
        result = cursor.fetchall()
        for row in result:
            id = row[0]
    
        cursor.close()
        
    

    except sqlite3.Error as error:
        for arg in error.args:
          glob_error = glob_error + arg
    
    finally:
        
        if sqliteConnection:
            sqliteConnection.close()
        return id

def registertoblog(username, password):
    status = 0
    global glob_error
    glob_error = ''
    try:
        
        # Connect to DB and create a cursor
        sqliteConnection = sqlite3.connect('sql.db')
        
        #check if username is unavailable...
        cursor = sqliteConnection.cursor()
    
        sql = """SELECT User_ID 
                    from USERS 
                    where User_name = ?"""
        args = (username,)
        cursor = cursor.execute(sql, args)
    
        result = cursor.fetchall()
        cursor.close()
        if len(result) > 0:
           status = -1
           glob_error = "Username unavailable"
           return status
    
 
        # insert the new user
        cursor = sqliteConnection.cursor()
    
        sql = """insert into USERS 
                (User_ID, User_name, User_Password) 
                values((select max(User_ID) from USERS) +1,?,?)"""
        args = (username,password)
        cursor = cursor.execute(sql, args)
    
        status = 1

        cursor.close()
        sqliteConnection.commit()

    except sqlite3.Error as error:
        for arg in error.args:
          glob_error = glob_error + arg
        status = -1
    
    finally:
        
        if sqliteConnection:
            sqliteConnection.close()
        return status
        
def post_blog(userid, content):
    status = 0
    global glob_error
    glob_error = ''
    try:
        
        # Connect to DB and create a cursor
        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()
    
        sql = """insert into POSTS 
                (Post_id,User_Name, Content) 
                values((select max(Post_id) from POSTS) +1,
                (select User_Name from USERS where User_ID = ?),?)"""
        args = (userid,content)
        cursor = cursor.execute(sql, args)
    
        status = 1

        cursor.close()
        sqliteConnection.commit()

    except sqlite3.Error as error:
        for arg in error.args:
          glob_error = glob_error + arg
        status = -1
    
    finally:
        
        if sqliteConnection:
            sqliteConnection.close()
        return status


def Get_posts():
    id = 0
    global glob_error
    glob_error = ''
    try:
        
        # Connect to DB and create a cursor
        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()
    
        sql = """SELECT User_Name,
                        Content 
                 from POSTS"""

        cursor = cursor.execute(sql)
    
        result = cursor.fetchall()
    
        cursor.close()
        
    

    except sqlite3.Error as error:
        for arg in error.args:
          glob_error = glob_error + arg
    
    finally:
        
        if sqliteConnection:
            sqliteConnection.close()
        return result


def Get_My_posts(id):
    global glob_error
    glob_error = ''
    try:
        
        # Connect to DB and create a cursor
        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()
    
        sql = """SELECT User_Name
                 from USERS
                 where User_ID = ?"""

        cursor = cursor.execute(sql,(id,))
        result = cursor.fetchone()
        username = result[0]
        cursor.close()

        cursor = sqliteConnection.cursor()
        sql = """SELECT Content,
                 User_Name
                 from POSTS
                 where User_Name = '{0}'"""
        
        
        cursor = cursor.execute((sql).format(username))
        result = cursor.fetchall()
        username = result[0]
        cursor.close()

    except sqlite3.Error as error:
        for arg in error.args:
          glob_error = glob_error + arg
    
    finally:
        
        if sqliteConnection:
            sqliteConnection.close()
        return result
    



def unsanitize(data):
    data = data.replace("&#x27;","'")
    data = data.replace("&quot;",'"')
    return data



app = Flask(__name__)



@app.route('/', methods=['GET'])
def index():
  return app.send_static_file('index.html')

@app.route('/blog', methods=['GET'])
def blog():
  if(isLogedIn):
    return app.send_static_file('blog.html')
  else:
    return redirect('/', 302)

@app.route('/fetch_posts', methods=['GET'])
def fetch_posts():
  if(not isLogedIn):
    return redirect('/', 302)
  
  posts = Get_posts()
  global glob_error
  if(glob_error != ''):
    return glob_error

  poststring = ""
  poststring = '''<!DOCTYPE html><html lang="en"><head>  <meta charset="utf-8">  <meta http-equiv="X-UA-Compatible" content="IE=edge">   <meta name="viewport" content="width=device-width, initial-scale=1.0">  <title>Blogg</title>  <link rel="stylesheet" type="text/css" href="static/css/style.css">  <link rel="stylesheet" type="text/css" href="static/css/sakura-dark-solarized.css">  <script src="static/js/fetchPosts.js"></script></head><body>'''
  for post in posts:
    poststring = poststring + ('<h2>posted by: {0}</h2><p>{1}</p>').format(post[0],post[1])

  poststring = poststring + '''</body>  </html>'''

  return poststring

@app.route('/fetch_my_posts', methods=['GET'])
def fetch_my_posts():
  if(not isLogedIn):
    return redirect('/', 302)
  global id
  posts = Get_My_posts(id)
  global glob_error
  if(glob_error != ''):
    return glob_error, 500

  

  poststring = ""
  poststring = '''<!DOCTYPE html><html lang="en"><head>  <meta charset="utf-8">  <meta http-equiv="X-UA-Compatible" content="IE=edge">   <meta name="viewport" content="width=device-width, initial-scale=1.0">  <title>Blogg</title>  <link rel="stylesheet" type="text/css" href="static/css/style.css">  <link rel="stylesheet" type="text/css" href="static/css/sakura-dark-solarized.css">  <script src="static/js/fetchPosts.js"></script></head><body>'''
  for post in posts:
    poststring = poststring + ('<h2>posted by: {0}</h2><p>{1}</p>').format(post[1],post[0])

  poststring = poststring + '''</body>  </html>'''
  return poststring, 200

@app.route('/login', methods=['POST', 'GET'])
def login():
  if request.method == 'GET':
    return app.send_static_file('login.html')
  elif request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    global id
    id = logintoblog(username,password)
    if(id != 0):
      # successful
      global isLogedIn 
      isLogedIn = True
      return redirect('/blog', 302)
    else:
      global glob_error
      if(glob_error == ""):
        return 'bad username/password', 400
      else:
        return glob_error, 400

@app.route('/logout', methods=['GET'])
def logout():

  global isLogedIn 
  global id
  isLogedIn = False
  id = 0

  return redirect('/', 302)

@app.route('/register', methods=['POST', 'GET'])
def register():
  if request.method == 'GET':
    return app.send_static_file('register.html')
  elif request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    
    sanitizedusername = html.escape(username)
    sanitizedPassword = html.escape(password)
    
    unsanitizedusername = unsanitize(sanitizedusername)
    unsanitizedpassword = unsanitize(sanitizedPassword)
    

    status = registertoblog(unsanitizedusername,unsanitizedpassword)
    if(status == 1):
      # if successful
      return redirect('/', 302)
    else:
      global glob_error
      return glob_error, 400

@app.route('/post', methods=['POST'])
def post():
  if(not isLogedIn):
    return redirect('/', 302)
  data = request.form['post']
  
  
  sanitizedData = html.escape(data)
  unsanitizeddata = unsanitize(sanitizedData)
  
  global id
  status = post_blog(id,unsanitizeddata)
  if(status == 1):
    # on success
    return 'Posten är inlagd.', 200
  else:
    # unsuccessful
    global glob_error
    return glob_error, 500

if __name__ == '__main__':
  from waitress import serve
  serve(app, host='0.0.0.0', port=1337)