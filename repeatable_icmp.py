import sys
from scapy.all import *

##
# 指定回数連続してICMPエコーを１つのホストに送信する。
# Usage: python %s source_ip target_ip repeat iface [type]
#   - source_ipにrange指定が可能:(ex. 192.168.10.1-255) 
#   - icmp_typeは既定で"echo-request"。"echo-reply"を指定
##
USAGE = "Usage: # python %s source_ip target_ip repeat iface [icmp_type]"
args = sys.argv
argc = len(args)
if (argc < 5):
    print(USAGE % args[0])
    quit()

source_ip=args[1]
if(source_ip == "help"):
    print(USAGE % args[0])
    quit()
target_ip=args[2]
repeat=args[3]
iface = args[4]
icmp_type = "echo-request"
if (argc >= 6):
    icmp_type = args[5]

print("source_ip:" + source_ip)
print("target_ip:" + target_ip)
print("repeat:" + repeat)
print("iface:" + iface)
print("icmp_type:" + icmp_type)

for i in range(int(repeat)):
    pkt = IP(src=source_ip, dst = target_ip) / ICMP(type = icmp_type)
    send(pkt, iface=iface)
