import item

class Room:
    def __init__(self):
        self.myDesc = """Det här är ett rum.\n"""
        self.myItem = [["marken", "Du står på den! Puh! En stund var du inte helt säker.\n"]]   # Pairs of [ item, description ]
        
    def setDesc(self,str):
        self.myDesc = str
        
    def queryLook(self):
        return self.myDesc

    def addItem(self,str,desc):
        for i in self.myItem:
            if i[0] == str:
                i[1] = desc
                return
        self.myItem += [[str, desc]]

    def removeItem(self,str):
        for i in self.myItem:
            if i[0] == str:
                self.myItem.remove(i)
                return


    def queryItem(self,str):
        for i in self.myItem:
            substr = i[0].split("|")
            for n in substr:
                if n == str:
                    return i[1]
        return        

    def take(self,plr,str):
        if self.queryItem(str):
            return "Det blir för mycket att släpa på, det är nog bäst att du låter den vara.\n"
        return 
    
    def say(self,plr,str):
        return

    def queryAction(self,plr,str):
        substr = str.split(" ",1)
        if not substr:
            return 
        if substr[0] == "sök" or substr[0] == "leta":
            if len(substr) < 2:
                return "Sök/leta på/i/bland vad?\n"
            substr = substr[1].split(" ",1)
            if not substr:
                return "Sök/leta på/i/bland vad?\n"
            if substr[0] == "på" or substr[0] == "i" or substr[0] == "bland":
                if len(substr) < 2:
                    return "Sök/leta på/i/bland vad?\n"
                if substr[1] == "rummet":
                    return "Du letar men hittar inget speciellt. Du kanske måste leta bland någon speciellt som finns i rummet.\n"
                if self.queryItem(substr[1]):
                    return "Du letar men hittar inget speciellt.\n"
                return f'Du ser inte {substr[1]} att leta {substr[0]}.\n'
        return 
    
    # Returns <direction>, <message>
    #   0 - No movement (fail)
    #   1 - Movenent forward
    #   2 - Movement backward
    def move(self,str):
        return 0, "Du kan inte gå åt det hållet.\n"

