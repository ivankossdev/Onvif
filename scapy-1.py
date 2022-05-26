from past.builtins import raw_input
from scapy.interfaces import show_interfaces
from scapy.layers.inet import *
from scapy.layers.l2 import *
from scapy.sendrecv import sniff
from scapy.utils import wrpcap


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


def whohas(ip):
    ans = arping(ip, verbose=False)[0]
    if not ans:
        return None
    return ans[0][1].hwsrc
print(whohas("192.168.0.250"))

# print(show_interfaces())
# lan = "Realtek PCIe GBE Family Controller"
# pkts = sniff(iface=lan,count=3,filter='arp')
# wrpcap("pkts.pcap", pkts)
#
#
# package = sniff(offline='pkts.pcap')
# print(package[0].show())
#
# # Имитировать отправку пакетов, отправку пакетов по всей сети, если есть ответ, значит активный хост
# p = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst='192.168.0.0/24')
# # ans представляет собой ответ полученного пакета
# ans, unans = srp(p, iface=lan, timeout=5)
#
# print("Всего просканировано% d хостов:" % len(ans))
#
# # Сохранить требуемый IP-адрес и Mac-адрес в списке результатов
# result = []
# for s, r in ans:
#     # Проанализировать полученный пакет и извлечь требуемый IP-адрес и MAC-адрес
#     result.append([r[ARP].psrc, r[ARP].hwsrc])
# # Отсортируйте полученную информацию, чтобы она выглядела более аккуратно
# result.sort()
# # Распечатать хост в LAN
# for ip, mac in result:
#     print(ip, '------>', mac)
