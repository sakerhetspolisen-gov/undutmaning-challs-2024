import utils
import gameinstance
import player
import hbsql
import signal
import os, uuid

welcomeText = """,-----------------------------------------------------------------------------.
|                       Välkommen till \"Stugan Revisited\"                     |
>-----------------------------------------------------------------------------<
|  Du befinner dig på ett hemligt uppdrag till Harald Blåtands sommarstuga.   |
|                                                                             |
| Om det här är den första gången du är på ett äventyr i en värld av text så  |
|   kanske du kan behöva lite tips - Läs hjälptexten. Titta på allt. Leta i   |
|  texten efter ledtrådar på vad du kan göra. Sök igenom det du ser som kan   |
|             verka dölja någon okänd hemlighet. Lycka till!                  |
'-----------------------------------------------------------------------------'\n"""

dbFileName = str(uuid.uuid4())

def main():
    newPlayer = player.Player(dbFileName)
    utils.out(welcomeText)

    # Delete any possibly corrupted DB:s
    if os.path.exists(dbFileName):
        os.remove(dbFileName)

    # Reset/create database
    hbsql.prepareDB(newPlayer)

    gameinstance.startGameInstance(newPlayer)

try:
    if __name__ == "__main__":
        main()
finally:
    if os.path.exists(dbFileName):
        os.remove(dbFileName)


