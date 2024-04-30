import sys

class Item:
    def __init__(self,iid,name,desc):
        self.myID = iid
        self.myName = name
        self.myDesc = desc

    def queryID(self,iid):
        substr = self.myID.split("|")
        for n in substr:
            if n == iid:
                return True
        return False       

    def queryAction(self,plr,str):
        return

    def queryName(self):
        return self.myName

    def queryDesc(self):
        return self.myDesc

class ReadItem(Item):
    def __init__(self,iid,name,desc,text):
        super().__init__(iid,name,desc)
        self.myText = text
    
    def flagFound(self,plr):
        return

    def queryAction(self,plr,str):
        substr = str.split(" ",1)
        if not substr:
            return 
        if substr[0] == "läs":
            if len(substr) < 2:
                return "Läs på/från vad?\n"
            substr = substr[1].split(" ",1)
            if not substr:
                return "Läs på/från vad?\n"
            if substr[0] == "på" or substr[0] == "från":
                if len(substr) < 2:
                    return "Läs på/från vad?\n"
                if self.queryID(substr[1]):
                    self.flagFound(plr)
                    return self.myText
                return 
            if self.queryID(substr[0]):
                self.flagFound(plr)
                return self.myText
        return super().queryAction(plr,str)