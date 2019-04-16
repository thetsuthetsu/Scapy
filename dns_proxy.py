import sys
from time import sleep
from scapy.all import *

##
# DNSリクエストを受信し、DNS応答を指定時間後にクライアントに応答する。
# "Usage: # python %s proxy_ip dns_ip wait(sec) iface src_ip [fromfilter_qname]"
##
USAGE = "Usage: # python %s proxy_ip dns_ip wait(sec) iface src_ip [filter_qname]"
dns_port = 53
args = sys.argv
argc = len(args)
if (argc < 6):
    print(USAGE % args[0])
    quit()

proxy_ip=args[1]
if(proxy_ip == "help"):
    print(USAGE % args[0])
    quit()

dns_ip=args[2]
wait = args[3]
iface = args[4]
src_ip = args[5]
filter_qname = ""
if (argc > 6):
    filter_qname = args[6]

print(f"proxy_ip:{proxy_ip}")
print(f"dns_ip:{dns_ip}")
print(f"wait(sec):{wait}")
print(f"iface:{iface}")
print(f"src_ip:{src_ip}")
print(f"filter_qname:{filter_qname}")

BPF_FILTER = f"udp port {dns_port} and ip dst {proxy_ip} and ip src {src_ip}"


def forward_dns(orig_pkt: IP):
    if (
        DNS in orig_pkt and
        orig_pkt[DNS].opcode == 0 and
        orig_pkt[DNS].ancount == 0
    ):
        # このプロキシへの直接問い合わせの場合にフォワード実行
        qname = orig_pkt[DNSQR].qname.decode()

        print(f"Forwarding: {qname}")
        response = sr1(
                IP(dst=dns_ip)/
                    UDP(sport = orig_pkt[UDP].sport)/
                    DNS(rd=1, id=orig_pkt[DNS].id, qd=DNSQR(qname=orig_pkt[DNSQR].qname)),
                verbose=0,           
        )

        # 本来のDNS応答をproxy応答に変換
        resp_pkt = IP(dst=orig_pkt[IP].src, src=proxy_ip)/UDP(dport=orig_pkt[UDP].sport)/DNS()
        resp_pkt[DNS] = response[DNS]

        if filter_qname in qname :
            # 指定秒数待って応答
            print("waiting...%s(sec)" % wait)
            sleep(int(wait))

        send(resp_pkt, verbose=0)
        return f"Responding to {orig_pkt[IP].src}:{resp_pkt[DNS].summary()}"

print("sniffing..." + BPF_FILTER)
sniff(filter=BPF_FILTER, prn=forward_dns, iface=iface)            