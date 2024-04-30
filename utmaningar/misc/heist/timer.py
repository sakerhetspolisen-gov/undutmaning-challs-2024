import curses
import threading
import time
import os

def countdown(win_countdown, stop_event, valid_command_event, timeout=12):
    ascii_art = [
        """
 _  ___  
/ |/ _ \ 
| | | | |
| | |_| |
|_|\___/
""",
     """
  ___  
 / _ \ 
| (_) |
 \__, |
   /_/ 
""",
     """
  ___  
 ( _ ) 
 / _ \ 
| (_) |
 \___/ 
""",
     """
 _____ 
|___  |
   / / 
  / /  
 /_/   
""",
     """
  __   
 / /_  
| '_ \ 
| (_) |
 \___/ 
""",
     """
 ____  
| ___| 
|___ \ 
 ___) |
|____/ 
""",
      """
 _  _   
| || |  
| || |_ 
|__   _|
   |_|  
""",
       """
 _____ 
|___ / 
  |_ \ 
 ___) |
|____/ 
""",
        """
 ____  
|___ \ 
  __) |
 / __/ 
|_____|
""",
        """
 _ 
/ |
| |
| |
|_|
""",
        """
  ___  
 / _ \ 
| | | |
| |_| |
 \___/ 
""",
        """
  ___  _   _ _____    ___  _____   _____ ___ __  __ _____ _ 
 / _ \| | | |_   _|  / _ \|  ___| |_   _|_ _|  \/  | ____| |
| | | | | | | | |   | | | | |_      | |  | || |\/| |  _| | |
| |_| | |_| | | |   | |_| |  _|     | |  | || |  | | |___|_|
 \___/ \___/  |_|    \___/|_|       |_| |___|_|  |_|_____(_)
"""
    ]

    art_index = -1
    start_time = time.time()
    elapsed_time = 0
    time.sleep(1)

    while timeout > 0:
        time.sleep(0.1)

        if stop_event.is_set():
            display_message(win_countdown, "RESET..")
            break

        if valid_command_event.is_set():
            win_countdown.refresh()
            while valid_command_event.is_set() and not stop_event.is_set():
                time.sleep(0.1)
            if not stop_event.is_set():
                display_message(win_countdown, "")
                start_time = time.time() - elapsed_time
            continue

        current_time = time.time()
        new_elapsed_time = current_time - start_time

        if new_elapsed_time - elapsed_time >= 1:
            elapsed_time = new_elapsed_time
            timeout -= 1
            art_index = (art_index + 1) % len(ascii_art)
            display_art(win_countdown, ascii_art[art_index])

    if timeout <= 0:
        display_art(win_countdown, ascii_art[-1]) 
        stop_event.set()
        time.sleep(5) 

def display_art(win, art):
    win.clear()
    try:
        for idx, line in enumerate(art.split('\n')):
            win.addstr(idx, 0, line)
    except curses.error:
        pass
    win.refresh()

def display_message(win, message):
    win.clear()
    try:
        win.addstr(0, 0, message)
        time.sleep(2)
    except curses.error:
        pass
    win.refresh()


def is_valid_tar_command(cmd):
    """Check if a command is a valid tar command."""
    valid_starts = ['tar -xf secret.tar', 'tar xf secret.tar']
    return any(cmd.startswith(valid_start) for valid_start in valid_starts)

def handle_input(win_input, win_error, valid_command_event, stop_event):
    ascii_error = """
  ____  _____ _____ ____  _   ____  _____ _____ ____  _   ____  _____ _____ ____  _
 | __ )| ____| ____|  _ \| | | __ )| ____| ____|  _ \| | | __ )| ____| ____|  _ \| |
 |  _ \|  _| |  _| | |_) | | |  _ \|  _| |  _| | |_) | | |  _ \|  _| |  _| | |_) | |
 | |_) | |___| |___|  __/|_| | |_) | |___| |___|  __/|_| | |_) | |___| |___|  __/|_|
 |____/|_____|_____|_|   (_) |____/|_____|_____|_|   (_) |____/|_____|_____|_|   (_)
 """
    win_input.nodelay(True)
    cmd = ""
    win_input.clear()
    win_input.addstr("Enter tar command to unpack secret.tar: ")
    win_input.refresh()

    while not stop_event.is_set():
        ch = win_input.getch()
        if ch == -1:
            time.sleep(0.1) 
            continue
        if ch == 10:  # Enter key
            if is_valid_tar_command(cmd):
                valid_command_event.set()
                break
            else:
                win_error.clear()
                try:
                    for idx, line in enumerate(ascii_error.split('\n')):
                        win_error.addstr(idx, 0, line)
                except curses.error as e:
                    pass
#                win_error.addstr("Invalid command. Please try again in 1 minute")
                win_error.refresh()
                stop_event.set()
                time.sleep(5)
                break 
        elif ch == 27:
            stop_event.set()
            break
        else:
            cmd += chr(ch) if 32 <= ch <= 126 else ''
    win_input.clear()
    win_error.clear()
    win_input.refresh()
    win_error.refresh()


def draw_menu(stdscr, valid_command_event, stop_event):
    height, width = stdscr.getmaxyx()
    win_countdown = curses.newwin(height // 2, width, 0, 0)
    win_input = curses.newwin(height //2, width, height // 2, 0)
    win_error = curses.newwin(height //2, width, height // 2, 0)

    # start countdown
    threading.Thread(target=countdown, args=(win_countdown, stop_event, valid_command_event), daemon=True).start()

    handle_input(win_input, win_error, valid_command_event, stop_event)

    if not valid_command_event.is_set() and stop_event.is_set():
        win_countdown.clear()
        win_countdown.refresh()

def prompt_user(stdscr):
    stdscr.clear()
    stdscr.addstr("Ready? If so, just type 'yes' to proceed: ")
    stdscr.refresh()
    response = stdscr.getstr().decode().strip().lower()
    stdscr.clear()
    stdscr.refresh()
    
    return response == "yes"

def main(stdscr):
    ascii_success = """
  _   _ _   _ _     ___   ____ _  _______ ____  _
 | | | | \ | | |   / _ \ / ___| |/ / ____|  _ \| |
 | | | |  \| | |  | | | | |   | ' /|  _| | | | | |
 | |_| | |\  | |__| |_| | |___| . \| |___| |_| |_|
  \___/|_| \_|_____\___/ \____|_|\_\_____|____/(_)
"""
    curses.curs_set(0)  # Hide cursor
    while True:
        if prompt_user(stdscr):
            stop_event = threading.Event()
            valid_command_event = threading.Event()
            draw_menu(stdscr, valid_command_event, stop_event)

            if valid_command_event.is_set():
                try:
                    for idx, line in enumerate(ascii_success.split('\n')):
                        stdscr.addstr(idx, 0, line)
                except curses.error as e:
                    pass
                stdscr.refresh()
                time.sleep(4)
                stdscr.clear()
                stdscr.refresh()
                try:
                    stdscr.addstr(0, 0, "Welcome Harald!" + "\n" + "\n" + "\n" +  "54 48 45 20 4b 45 59 20 69 73 20 75 6e 64 75 74 7b 75 6e 64 65 72 5f 70 72 65 73 73 75 72 65 5f 77 69 74 68 6f 75 74 5f 76 69 73 75 61 6c 5f 63 6f 6e 66 69 72 6d 61 74 69 6f 6e 7d" + "\n" + "\n" + "\n" + "\n" + "KILLING LOCKBOX!")
                    stdscr.refresh()
                except curses.error as e:
                    pass
                stdscr.refresh()
                stdscr.getch()
                os.system("sleep 5 && killall -u ctf")
                break

            if stop_event.is_set() and not valid_command_event.is_set():
                stdscr.clear()
                stdscr.refresh()
                continue 
        else:
            stdscr.addstr("Not ready, good choice, lets make a plan")
            stdscr.refresh()
            time.sleep(2)

if __name__ == "__main__":
    curses.wrapper(main)

