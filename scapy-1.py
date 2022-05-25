from past.builtins import raw_input
from scapy.layers.inet import *
from scapy.layers.l2 import *
b = IP()
print(raw(b))


def scan(ip):
    #My code
    print("Scanning...")
    arp_request=ARP(pdst=ip)
    brodcast=Ether(dst="ff:ff:ff:ff:ff:ff")
    arp=brodcast/arp_request
    answered=srp(arp, timeout=1,verbose=False)
    for element in answered:
        print(element)
        # print("IP:{}".format(element[1].psrc))
        # print("MAC address: {}\n".format(element[1].hwsrc))

def scan2(ip):
    #Code from scapy documentation and it's also not detecting any devices
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip),timeout=2)
    ans.summary(lambda s, r: r.sprintf("%Ether.src% %ARP.psrc%") )

scan('192.168.0.173')
scan2('192.168.0.173')
a = arping('192.168.0.173')
print(a)
