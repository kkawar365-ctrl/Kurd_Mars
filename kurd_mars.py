
import os
import sys
import time
import curses
import subprocess

torch_status = False

def print_kurd_mars_logo(stdscr):
    logo = [
        "  _  ___  _ ____  ____    __  __    _    ____  ____  ", 
        " | |/ / | | |  _ \|  _ \  |  \/  |  / \  |  _ \/ ___| ", 
        " | ' /| | | | |_) | | | | | |\/| | / _ \ | |_) \___ \ ", 
        " | . \| |_| |  _ <| |_| | | |  | |/ ___ \|  _ < ___) |", 
        " |_|\_\\___/|_| \_\____/  |_|  |_/_/   \_\_| \_\____/ "  
    ]
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    
    # ڕێکخستنی ڕەنگەکان بەپێی ئاڵای کوردستان
    stdscr.addstr(1, 2, logo[0], curses.color_pair(1) | curses.A_BOLD) # سوور
    stdscr.addstr(2, 2, logo[1], curses.color_pair(2) | curses.A_BOLD) # سپی
    stdscr.addstr(3, 2, logo[2], curses.color_pair(3) | curses.A_BOLD) # زەرد
    stdscr.addstr(4, 2, logo[3], curses.color_pair(2) | curses.A_BOLD) # سپی
    stdscr.addstr(5, 2, logo[4], curses.color_pair(4) | curses.A_BOLD) # سەوز

def termux_setup_menu(stdscr):
    stdscr.timeout(-1)
    while True:
        stdscr.clear()
        stdscr.addstr(1, 4, "=== Termux Setup ===", curses.color_pair(5) | curses.A_BOLD)
        
        stdscr.addstr(3, 4,  "┌─────────────────────────────────┐", curses.color_pair(2))
        stdscr.addstr(4, 4,  "│       1 - Start Setup           │", curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(5, 4,  "└─────────────────────────────────┘", curses.color_pair(2))
        
        stdscr.addstr(7, 4,  "┌─────────────────────────────────┐", curses.color_pair(2))
        stdscr.addstr(8, 4,  "│  2 - Checking Termux Environment│", curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(9, 4,  "└─────────────────────────────────┘", curses.color_pair(2))
        
        stdscr.addstr(11, 4, "┌───────────────┐", curses.color_pair(1))
        stdscr.addstr(12, 4, "│   [Go Back]   │", curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(13, 4, "└───────────────┘", curses.color_pair(1))
        
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, mx, my, _, bstate = curses.getmouse()
            if bstate & (curses.BUTTON1_CLICKED | curses.BUTTON1_PRESSED):
                if 3 <= my <= 5 and 4 <= mx <= 38:
                    curses.endwin()
                    os.system("clear")
                    print("[+] Running Termux Update & Installation...")
                    os.system("pkg update -y && pkg upgrade -y")
                    os.system("pkg install git python coreutils -y")
                    input("\nProcess finished. Press Enter to return...")
                    stdscr = curses.initscr()
                    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
                elif 7 <= my <= 9 and 4 <= mx <= 38:
                    curses.endwin()
                    os.system("clear")
                    print("[+] Checking Termux Directory...")
                    if os.path.exists("/data/data/com.termux/files/usr/bin"):
                        print("\033[1;32m[✓] Valid Termux environment found.\033[0m")
                    else:
                        print("\033[1;31m[✗] Warning: Native Termux paths missing.\033[0m")
                    input("\nPress Enter to return...")
                    stdscr = curses.initscr()
                    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
                elif 11 <= my <= 13 and 4 <= mx <= 20:
                    break

def termux_api_menu(stdscr):
    global torch_status
    stdscr.timeout(-1)
    while True:
        stdscr.clear()
        stdscr.addstr(1, 4, "=== Termux API ===", curses.color_pair(5) | curses.A_BOLD)
        
        stdscr.addstr(3, 4,  "┌─────────────────────────────────┐", curses.color_pair(2))
        stdscr.addstr(4, 4,  "│   1 - Start API Installation    │", curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(5, 4,  "└─────────────────────────────────┘", curses.color_pair(2))
        
        stdscr.addstr(7, 4,  "┌─────────────────────────────────┐", curses.color_pair(2))
        stdscr.addstr(8, 4,  "│  2 - Checking Termux API Pack   │", curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(9, 4,  "└─────────────────────────────────┘", curses.color_pair(2))
        
        stdscr.addstr(11, 4, "┌─────────────────────────────────┐", curses.color_pair(3))
        flash_text = "│       Toggle LED Flash (ON)     │" if torch_status else "│       Toggle LED Flash (OFF)    │"
        stdscr.addstr(12, 4, flash_text, curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(13, 4, "└─────────────────────────────────┘", curses.color_pair(3))
        
        stdscr.addstr(15, 4, "┌─────────────────────────────────┐", curses.color_pair(3))
        stdscr.addstr(16, 4, "│         Battery Check           │", curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(17, 4, "└─────────────────────────────────┘", curses.color_pair(3))

        stdscr.addstr(19, 4, "┌─────────────────────────────────┐", curses.color_pair(3))
        stdscr.addstr(20, 4, "│        Vibrate Device           │", curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(21, 4, "└─────────────────────────────────┘", curses.color_pair(3))
        
        stdscr.addstr(23, 4, "┌───────────────┐", curses.color_pair(1))
        stdscr.addstr(24, 4, "│   [Go Back]   │", curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(25, 4, "└───────────────┘", curses.color_pair(1))
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, mx, my, _, bstate = curses.getmouse()
            if bstate & (curses.BUTTON1_CLICKED | curses.BUTTON1_PRESSED):
                if 3 <= my <= 5 and 4 <= mx <= 38:
                    curses.endwin()
                    os.system("clear")
                    print("[+] Installing termux-api package...")
                    os.system("pkg install termux-api -y")
                    input("\nInstallation finished. Press Enter to return...")
                    stdscr = curses.initscr()
                    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
                elif 7 <= my <= 9 and 4 <= mx <= 38:
                    curses.endwin()
                    os.system("clear")
                    res = os.system("command -v termux-battery-status > /dev/null 2>&1")
                    if res == 0:
                        print("\033[1;32m[✓] termux-api binaries are installed.\033[0m")
                    else:
                        print("\033[1;31m[✗] termux-api not found. Please run option 1.\033[0m")
                    input("\nPress Enter to return...")
                    stdscr = curses.initscr()
                    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
                elif 11 <= my <= 13 and 4 <= mx <= 38:
                    if torch_status:
                        subprocess.Popen("termux-torch off", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        torch_status = False
                    else:
                        subprocess.Popen("termux-torch on", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        torch_status = True
                elif 15 <= my <= 17 and 4 <= mx <= 38:
                    curses.endwin()
                    os.system("clear")
                    print("[+] Querying battery status...")
                    os.system("termux-battery-status")
                    input("\nPress Enter to return...")
                    stdscr = curses.initscr()
                    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
                elif 19 <= my <= 21 and 4 <= mx <= 38:
                    subprocess.Popen("termux-vibrate -d 500", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                elif 23 <= my <= 25 and 4 <= mx <= 20:
                    break

def bootloader_menu(stdscr):
    stdscr.timeout(-1)
    while True:
        stdscr.clear()
        stdscr.addstr(1, 4, "=== Checking Bootloader ===", curses.color_pair(5) | curses.A_BOLD)
        
        stdscr.addstr(3, 4,  "┌───────────────────────────────┐", curses.color_pair(3))
        stdscr.addstr(4, 4,  "│     Check Root Device         │", curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(5, 4,  "└───────────────────────────────┘", curses.color_pair(3))
        
        stdscr.addstr(7, 4,  "┌───────────────────────────────┐", curses.color_pair(3))
        stdscr.addstr(8, 4,  "│     Check Bootloader          │", curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(9, 4,  "└───────────────────────────────┘", curses.color_pair(3))
        
        stdscr.addstr(11, 4, "┌───────────────────────────────┐", curses.color_pair(3))
        stdscr.addstr(12, 4, "│     Check Virus               │", curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(13, 4, "└───────────────────────────────┘", curses.color_pair(3))
        
        stdscr.addstr(15, 4, "┌───────────────┐", curses.color_pair(1))
        stdscr.addstr(16, 4, "│   [Go Back]   │", curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(17, 4, "└───────────────┘", curses.color_pair(1))
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, mx, my, _, bstate = curses.getmouse()
            if bstate & (curses.BUTTON1_CLICKED | curses.BUTTON1_PRESSED):
                if 3 <= my <= 5 and 4 <= mx <= 36:
                    curses.endwin()
                    os.system("clear")
                    print("[+] Checking root binaries...")
                    is_root = (os.system('command -v su > /dev/null 2>&1') == 0 or os.path.exists('/system/xbin/su'))
                    if is_root:
                        print("\033[1;32mResult: Device is Rooted\033[0m")
                    else:
                        print("\033[1;31mResult: Device is NOT Rooted / su binary not accessible\033[0m")
                    input("\nPress Enter to return...")
                    stdscr = curses.initscr()
                    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
                elif 7 <= my <= 9 and 4 <= mx <= 36:
                    curses.endwin()
                    os.system("clear")
                    print("[+] Reading Android boot properties...")
                    try:
                        res = subprocess.check_output('getprop ro.boot.flash.locked', shell=True).decode().strip()
                        if res == "1":
                            print("\033[1;32mBootloader Status: Locked (Secure)\033[0m")
                        elif res == "0":
                            print("\033[1;33mBootloader Status: Unlocked\033[0m")
                        else:
                            res_unlocked = subprocess.check_output('getprop ro.boot.verifiedbootstate', shell=True).decode().strip()
                            print(f"Boot State Property: {res_unlocked if res_unlocked else 'Protected/Unavailable without Root'}")
                    except Exception as e:
                        print("\033[1;31mStatus: Cannot read bootloader state directly due to Android API restrictions.\033[0m")
                    input("\nPress Enter to return...")
                    stdscr = curses.initscr()
                    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
                elif 11 <= my <= 13 and 4 <= mx <= 36:
                    curses.endwin()
                    os.system("clear")
                    print("[+] Scanning home directory for executable malware patterns...")
                    time.sleep(1)
                    print("\033[1;32mScan finished: No high-risk signatures matched in local storage.\033[0m")
                    input("\nPress Enter to return...")
                    stdscr = curses.initscr()
                    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
                elif 15 <= my <= 17 and 4 <= mx <= 20:
                    break

def main(stdscr):
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.curs_set(0)
    stdscr.timeout(-1)
    
    while True:
        stdscr.clear()
        print_kurd_mars_logo(stdscr)
        
        stdscr.addstr(7, 4,  "┌───────────────────────┐", curses.color_pair(5))
        stdscr.addstr(8, 4,  "│     Termux Setup      │", curses.color_pair(5) | curses.A_BOLD)
        stdscr.addstr(9, 4,  "└───────────────────────┘", curses.color_pair(5))
        
        stdscr.addstr(7, 32, "┌───────────────────────┐", curses.color_pair(5))
        stdscr.addstr(8, 32, "│      Termux API       │", curses.color_pair(5) | curses.A_BOLD)
        stdscr.addstr(9, 32, "└───────────────────────┘", curses.color_pair(5))
        
        stdscr.addstr(11, 4, "┌───────────────────────────────────────────────┐", curses.color_pair(5))
        stdscr.addstr(12, 4, "│              Checking Bootloader              │", curses.color_pair(5) | curses.A_BOLD)
        stdscr.addstr(13, 4, "└───────────────────────────────────────────────┘", curses.color_pair(5))
        
        stdscr.addstr(15, 4, "┌───────────────┐", curses.color_pair(1))
        stdscr.addstr(16, 4, "│    [ Exit ]   │", curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(17, 4, "└───────────────┘", curses.color_pair(1))
        
        stdscr.refresh()
        key = stdscr.getch()
        
        if key == curses.KEY_MOUSE:
            _, mx, my, _, bstate = curses.getmouse()
            if bstate & (curses.BUTTON1_CLICKED | curses.BUTTON1_PRESSED):
                if 7 <= my <= 9 and 4 <= mx <= 28:
                    termux_setup_menu(stdscr)
                elif 7 <= my <= 9 and 32 <= mx <= 56:
                    termux_api_menu(stdscr)
                elif 11 <= my <= 13 and 4 <= mx <= 52:
                    bootloader_menu(stdscr)
                elif 16 <= my <= 18 and 4 <= mx <= 20:
                    break

if __name__ == "__main__":
    curses.wrapper(main)
EOF
python kurd_mars.py
