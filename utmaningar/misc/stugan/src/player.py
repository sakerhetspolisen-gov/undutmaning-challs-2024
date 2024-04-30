import item
import utils

class Player:
    def __init__(self,dbFileName):
        self.myInventory = []
        self.myDbFileName = dbFileName

    def getItem(self,iid):
        for i in self.myInventory:
            if i.queryID(iid):
                return i
        return        

    def showItem(self,str):
        i = self.getItem(str)
        if i:
            utils.out(i.queryDesc())
            return True
        return False

    def queryAction(self,str):
        for i in self.myInventory:
            msg = i.queryAction(self,str)
            if msg:
                return msg
        return

    def addItem(self,i):
        self.myInventory.append(i)

    def removeItem(self,i):
        self.myInventory.remove(i)        

    def showInventory(self):
        if len(self.myInventory) == 0:
            utils.out("Du bär inte med dig några saker än.\n")
            return
        msg = "Du bär på:\n"
        for i in self.myInventory:
            msg += i.queryName().capitalize() + "\n"
        utils.out(msg)
        return
