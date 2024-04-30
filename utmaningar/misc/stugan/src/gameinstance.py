import item
import room
import rooms
import player
import utils
import sys

helpText = """,-----------------------------------------------------------------------------.
| Kommandon:                                                                  |
|   titta          - Se dig omkring.                                          |
|   titta på <sak> - Titta närmare på något du ser omkring dig.               |
|   saker          - Kontrollera vad du bär med dig för saker.                |
|   sluta          - Lämna textvärlden och återvänd till verkligheten.        |
|   Övriga saker du kan göra i världen får du lista ut själv.                 |
|   OBS! Tänk på att ange verb i infinitiv och substantiv i bestämd form!     |
|        Exempel. > titta på stugan                                           |
|                 > leta i lådan                                              |
|                 > öppna dörren                                              |
`-----------------------------------------------------------------------------´\n"""

def startGameInstance(plr):
    roomList = [ rooms.Room1(), rooms.Room2(), rooms.Room3(), rooms.Room4() ]
    currentRoom = 0

    try:
        utils.out(roomList[currentRoom].queryLook())

        while True:
            # Send a prompt
            utils.out("Vad gör du? > ")
            data = sys.stdin.readline().strip().lower()

            if not data:
                continue

            # First check if the player has anything with him that has special commands
            msg = plr.queryAction(data)
            if msg:
                utils.out(msg)
                continue 

            # First let the room check if it is a special command
            msg = roomList[currentRoom].queryAction(plr,data)

            if msg:
                utils.out(msg)
                continue 

            commands = data.split(" ", 1)

            if commands[0] == "sluta":
                utils.out("Hej då!\n")
                del plr
                break

            if commands[0] == "saker":
                plr.showInventory()
                continue

            if commands[0] == "titta":
                if len(commands) < 2:
                    utils.out(roomList[currentRoom].queryLook())
                    continue
                args = commands[1].split(" ", 1)
                if not args or args[0] != "på" or len(args) < 2:
                    utils.out("Titta på vad?\n")
                    continue
                # First we check if any item matches
                if plr.showItem(args[1]):
                    continue
                # Then we check if the room matches
                msg = roomList[currentRoom].queryItem(args[1])
                if not msg:
                    utils.out(f'Du ser ingen \"{args[1]}\" här.\n')
                    continue
                utils.out(msg)
                continue

            if commands[0] == "hjälp":
                utils.out(helpText)
                continue

            if commands[0] == "ta":
                if len(commands) < 2:
                    utils.out("Ta vad?\n")
                    continue
                msg = roomList[currentRoom].take(plr,commands[1])
                if msg:
                    utils.out(msg)
                    continue
                utils.out(f'Du kan inte \"{data}\".\n')
                continue

            if commands[0] == "säg":
                if len(commands) < 2:
                    utils.out("Säg vad?\n")
                    continue
                msg = roomList[currentRoom].say(plr,commands[1])
                if msg:
                    utils.out(msg)
                    continue
                utils.out(f'Du säger: {commands[1].capitalize()}\n')
                continue
            

            if commands[0] == "gå":
                if len(commands) < 2:
                    utils.out("Gå var?\n")
                    continue
                m, msg = roomList[currentRoom].move(commands[1])
                if m == 0:
                    utils.out(msg)
                    continue
                if m == 1:
                    if currentRoom + 2 > len(roomList):
                        utils.out("Du kan inte gå dit.\n")
                        continue
                    currentRoom = currentRoom + 1
                    utils.out(msg)
                    utils.out(roomList[currentRoom].queryLook())
                    continue
                if m == 2:
                    if currentRoom == 0:
                        utils.out("Du kan inte gå dit.\n")
                        continue
                    currentRoom = currentRoom - 1
                    utils.out(msg)
                    utils.out(roomList[currentRoom].queryLook())
                    continue

            utils.out("Vad försöker du göra? Skriv \"hjälp\" för att få hjälp.\n")

    except Exception as e:
        utils.out("Något gick fel. Ursäkta!\n")
        del plr
        return

