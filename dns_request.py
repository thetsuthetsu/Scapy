import sys
from scapy.all import *

##
# DNSリクエストを送信し、応答を待つ。
# "Usage: # python %s dns_ip dns_qname iface"
##
USAGE = "Usage: # python %s dns_ip dns_qname iface"
dns_port = 53
args = sys.argv
argc = len(args)
if (argc < 4):
    print(USAGE % args[0])
    quit()

dns_ip=args[1]
if(dns_ip == "help"):
    print(USAGE % args[0])
    quit()
dns_qname = args[2]
iface = args[3]

print("dns_ip:" + dns_ip)
print("dns_qname:" + dns_qname)
print("iface:" + iface)

ip = IP(dst = dns_ip)
udp = UDP(dport = dns_port)
dns = DNS(rd=1, qd=DNSQR(qname=dns_qname))

dns_req = ip / udp / dns
answer = sr1(dns_req, verbose=0, iface=iface)
print(answer[DNS].summary())