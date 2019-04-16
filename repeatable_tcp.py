import sys
from scapy.all import *

##
# 指定回数連続してTCPフラグを１つのホストに送信する。
# Usage: # python %s source_ip source_port target_ip target_port repeat iface flags [seq]
#   - source_ipにrange指定が可能:(ex. 192.168.10.1-255)
#   - flagsに任意のTCPフラグを指定可能：(ex. S/F/P/U/R/A)
#   - seqに任意のシーケンス番号を指定可能
##
USAGE = "Usage: # python %s source_ip source_port target_ip target_port repeat iface flags [seq]"
args = sys.argv
argc = len(args)
if (argc < 8):
    print(USAGE % args[0])
    quit()

source_ip=args[1]
if(source_ip == "help"):
    print(USAGE % args[0])
    quit()

source_port = args[2]
target_ip=args[3]
target_port=args[4]
repeat=args[5]
iface = args[6]
flags = args[7]
print("target_ip:" + target_ip)
print("target_port:" + target_port)
print("repeat:" + repeat)
print("iface:" + iface)
print("flags:" + flags)

ip = IP(src = source_ip, dst = target_ip)

if(argc > 8):
    seq = args[8]
    print("seq:" + seq)
    tcp = TCP(sport = int(source_port), dport = int(target_port), flags = flags, seq = int(seq))
else:    
    tcp = TCP(sport = int(source_port), dport = int(target_port), flags = flags)

for i in range(int(repeat)):
    send(ip / tcp, iface=iface, filter="tcp and ( port " + target_port + " )")

