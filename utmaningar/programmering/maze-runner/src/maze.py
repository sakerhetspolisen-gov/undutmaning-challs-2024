import signal
import generate
import sys

def out(text="", end="\n"):
    print(text, end=end)
    sys.stdout.flush()

def set_time_limit(seconds):
    def alarm(*_):
        out("Tiden tog slut!")
        raise SystemExit("Tiden tog slut!")
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(seconds)

def main():
    time_limit = 60
    current_pos = (0, 0)
    visibility = 0

    out("Haralds Trojaborg - Ta dig in om du kan!")
    out(" Hur modig är du?")
    out("  1. Hjälp, jag är rädd!")
    out("  2. Jag är inte lättskrämd.")
    out("  3. \"Utan fruktan\" är mitt mellannamn!")
    out("Skriv 'h' för hjälp.")

    while True:
        out("Skriv in ditt val: ",end="")
        data = sys.stdin.readline().strip().lower()
 
        if not data:
            return

        if data == "1":
            time_limit = 60
            width, height = 20, 20
            visibility = 0
            break
        elif data == "2":
            time_limit = 60
            width, height = 50, 50
            visibility = 20
            break
        elif data == "3":
            time_limit = 60
            width, height = 100, 100
            visibility = 10
            break
        elif data == "h":
            out(" \# - Vägg, hit kan du inte gå")
            out(" . - Korridor, här kan du gå")
            out(" * - Det här är du")
            out("Flytta: A för vänster, W för upp, S för ned och D för höger")
            out("Visa trojaborgen: E")
            out("Ge upp: Q")
        elif data == "q":
            out("Hej då!")
            return
        else:
            out("Ogiltigt val. Pröva igen!")

    maze = generate.Maze(width, height)
    out(f"Du är fast i Haralds Trojaborg. Du har {time_limit} sekunder på dig. Börja spring!")
    maze.print(visibility)
    set_time_limit(time_limit) 

    while not maze.goal():
        out("Flytta (A,W,S,D): ",end="")
        data = sys.stdin.readline().strip().lower()

        if not data or data == 'e':
            maze.print(visibility)
            continue

        if data == 'q':
            return

        if not maze.move(data):
            out("Du kan inte gå åt det hållet. Försök igen.")
            continue

        # Dont show maze each time..
        # maze.print(visibility)

    out("Grattis, du klarade det!")

    if width < 100:
        out("Du kanske ska prova på något svårare nästa gång!")
    else:
        f = open("flag.txt","r")
        text = f.read()
        f.close()
        out(f"Här får du en kaka: {text}")

    out("Hej då! Välkommen åter!")

if __name__ == "__main__":
    main()

